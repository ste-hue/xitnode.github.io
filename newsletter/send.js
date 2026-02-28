const fs = require("fs");
const path = require("path");
const matter = require("gray-matter");
const { marked } = require("marked");
const { Resend } = require("resend");

const POSTS_DIR = path.join(__dirname, "..", "_posts");
const TEMPLATE_PATH = path.join(__dirname, "email-template.html");
const SITE_URL = "https://xitnode.com";

function getPostFiles() {
  return fs
    .readdirSync(POSTS_DIR)
    .filter((f) => f.endsWith(".md"))
    .sort();
}

function findPost(slug) {
  const files = getPostFiles();
  if (slug) {
    const match = files.find((f) => f.includes(slug));
    if (!match) {
      console.error(`No post found matching slug: ${slug}`);
      process.exit(1);
    }
    return match;
  }
  return files[files.length - 1];
}

function parsePost(filename) {
  const filepath = path.join(POSTS_DIR, filename);
  const raw = fs.readFileSync(filepath, "utf-8");
  const { data, content } = matter(raw);

  const dateMatch = filename.match(/^(\d{4}-\d{2}-\d{2})/);
  const dateStr = data.date
    ? new Date(data.date).toLocaleDateString("it-IT", {
        year: "numeric",
        month: "long",
        day: "numeric",
      })
    : dateMatch
      ? new Date(dateMatch[1] + "T12:00:00").toLocaleDateString("it-IT", {
          year: "numeric",
          month: "long",
          day: "numeric",
        })
      : "";

  const slugPart = filename.replace(/^\d{4}-\d{2}-\d{2}-/, "").replace(/\.md$/, "");
  const yearMatch = filename.match(/^(\d{4})/);
  const monthMatch = filename.match(/^\d{4}-(\d{2})/);
  const dayMatch = filename.match(/^\d{4}-\d{2}-(\d{2})/);
  const postUrl = `${SITE_URL}/${yearMatch[1]}/${monthMatch[1]}/${dayMatch[1]}/${slugPart}`;

  const htmlContent = marked(content);

  return {
    title: data.title || slugPart,
    date: dateStr,
    content: htmlContent,
    postUrl,
    year: new Date().getFullYear().toString(),
  };
}

function renderEmail(post) {
  let template = fs.readFileSync(TEMPLATE_PATH, "utf-8");
  template = template.replace(/\{\{TITLE\}\}/g, post.title);
  template = template.replace(/\{\{DATE\}\}/g, post.date);
  template = template.replace(/\{\{CONTENT\}\}/g, post.content);
  template = template.replace(/\{\{POST_URL\}\}/g, post.postUrl);
  template = template.replace(/\{\{YEAR\}\}/g, post.year);
  return template;
}

async function sendNewsletter(html, post, dryRun) {
  if (dryRun) {
    console.log("--- DRY RUN ---");
    console.log(`Subject: ${post.title}`);
    console.log(`Post URL: ${post.postUrl}`);
    console.log(`HTML length: ${html.length} chars`);
    console.log("Email rendered successfully. No email sent.");
    return;
  }

  const apiKey = process.env.RESEND_API_KEY;
  const audienceId = process.env.RESEND_AUDIENCE_ID;

  if (!apiKey || !audienceId) {
    console.error("Missing RESEND_API_KEY or RESEND_AUDIENCE_ID environment variables.");
    process.exit(1);
  }

  const resend = new Resend(apiKey);

  const broadcast = await resend.broadcasts.create({
    audienceId,
    from: "xitnode <newsletter@xitnode.com>",
    subject: post.title,
    html,
  });

  if (broadcast.error) {
    console.error("Failed to create broadcast:", broadcast.error);
    process.exit(1);
  }

  console.log(`Broadcast created: ${broadcast.data.id}`);

  const sent = await resend.broadcasts.send(broadcast.data.id);

  if (sent.error) {
    console.error("Failed to send broadcast:", sent.error);
    process.exit(1);
  }

  console.log(`Newsletter sent successfully: "${post.title}"`);
}

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes("--dry-run");
  const slugFlag = args.indexOf("--slug");
  const slug = slugFlag !== -1 ? args[slugFlag + 1] : null;

  const filename = findPost(slug);
  console.log(`Processing: ${filename}`);

  const post = parsePost(filename);
  const html = renderEmail(post);

  await sendNewsletter(html, post, dryRun);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
