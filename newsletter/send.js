require("dotenv").config();
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const matter = require("gray-matter");
const { marked } = require("marked");
const { Resend } = require("resend");
const sharp = require("sharp");

const POSTS_DIR = path.join(__dirname, "..", "_posts");
const TEMPLATE_PATH = path.join(__dirname, "email-template.html");
const TRACKER_PATH = path.join(__dirname, "last-sent.json");
const EMAIL_ASSETS_DIR = path.join(__dirname, "..", "assets", "email");
const SITE_URL = "https://xitnode.com";

function getPostFiles() {
  return fs
    .readdirSync(POSTS_DIR)
    .filter((f) => f.endsWith(".md"))
    .sort();
}

function getPostDate(filename) {
  const match = filename.match(/^(\d{4}-\d{2}-\d{2})/);
  return match ? match[1] : null;
}

function getPostsSince(sinceDate) {
  return getPostFiles().filter((f) => {
    const date = getPostDate(f);
    return date && date > sinceDate;
  });
}

function readTracker() {
  if (!fs.existsSync(TRACKER_PATH)) {
    return { lastSentDate: "1970-01-01" };
  }
  return JSON.parse(fs.readFileSync(TRACKER_PATH, "utf-8"));
}

function updateTracker(filename) {
  const today = new Date().toISOString().split("T")[0];
  const data = { lastSentDate: today, lastSentFile: filename };
  fs.writeFileSync(TRACKER_PATH, JSON.stringify(data, null, 2) + "\n");
  console.log(`Tracker updated: lastSentDate = ${today}, lastSentFile = ${filename}`);
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
  const categories = Array.isArray(data.categories) ? data.categories : [];
  const categoryPath = categories.length > 0 ? categories.join("/") + "/" : "";
  const postUrl = `${SITE_URL}/${categoryPath}${yearMatch[1]}/${monthMatch[1]}/${dayMatch[1]}/${slugPart}.html`;

  const htmlContent = marked(content);

  return {
    title: data.title || slugPart,
    date: dateStr,
    content: htmlContent,
    postUrl,
    year: new Date().getFullYear().toString(),
  };
}

async function convertSvgsForEmail(html, postUrl) {
  fs.mkdirSync(EMAIL_ASSETS_DIR, { recursive: true });

  const svgRegex = /(?:<figure>\s*)?<svg[\s\S]*?<\/svg>(?:\s*<\/figure>)?/gi;
  const matches = [...html.matchAll(svgRegex)];

  if (matches.length === 0) return { html, generatedFiles: [] };

  const generatedFiles = [];

  for (let i = 0; i < matches.length; i++) {
    const svgMatch = matches[i][0];
    // Extract just the <svg>...</svg> portion
    const svgOnly = svgMatch.match(/<svg[\s\S]*?<\/svg>/i)?.[0];
    if (!svgOnly) continue;

    const hash = crypto.createHash("md5").update(svgOnly).digest("hex").slice(0, 10);
    const filename = `diagram-${hash}.png`;
    const filepath = path.join(EMAIL_ASSETS_DIR, filename);

    try {
      // Render SVG to PNG at 2x for retina sharpness
      const pngBuffer = await sharp(Buffer.from(svgOnly))
        .png()
        .resize({ width: 1080, withoutEnlargement: true })
        .toBuffer();

      fs.writeFileSync(filepath, pngBuffer);
      generatedFiles.push(filepath);

      const imgUrl = `${SITE_URL}/assets/email/${filename}`;
      const imgTag = `<img src="${imgUrl}" alt="Diagramma" style="max-width:100%;height:auto;border:1px solid #eee;border-radius:4px;" />`;
      html = html.replace(svgMatch, imgTag);

      console.log(`  SVG ${i + 1}/${matches.length} → ${filename} (${(pngBuffer.length / 1024).toFixed(1)}KB)`);
    } catch (err) {
      console.warn(`  SVG ${i + 1}/${matches.length} conversion failed, using fallback link:`, err.message);
      const fallback = `<p style="padding:16px;background:#f5f5f5;border:1px solid #ddd;border-radius:4px;text-align:center;color:#666;font-size:14px;">[Diagramma — <a href="${postUrl}" style="color:#007acc;">vedi sul sito</a>]</p>`;
      html = html.replace(svgMatch, fallback);
    }
  }

  return { html, generatedFiles };
}

async function renderEmail(post) {
  let template = fs.readFileSync(TEMPLATE_PATH, "utf-8");
  const { html: content, generatedFiles } = await convertSvgsForEmail(post.content, post.postUrl);
  template = template.replace(/\{\{TITLE\}\}/g, post.title);
  template = template.replace(/\{\{DATE\}\}/g, post.date);
  template = template.replace(/\{\{CONTENT\}\}/g, content);
  template = template.replace(/\{\{POST_URL\}\}/g, post.postUrl);
  template = template.replace(/\{\{YEAR\}\}/g, post.year);
  return { html: template, generatedFiles };
}

async function sendNewsletter(html, post, { dryRun, testEmail }) {
  if (dryRun) {
    console.log("--- DRY RUN ---");
    console.log(`Subject: ${post.title}`);
    console.log(`Post URL: ${post.postUrl}`);
    console.log(`HTML length: ${html.length} chars`);
    console.log("Email rendered successfully. No email sent.");
    return;
  }

  const apiKey = process.env.RESEND_API_KEY;

  if (!apiKey) {
    console.error("Missing RESEND_API_KEY environment variable.");
    process.exit(1);
  }

  const resend = new Resend(apiKey);

  if (testEmail) {
    const result = await resend.emails.send({
      from: "xitnode <newsletter@xitnode.com>",
      to: testEmail,
      subject: `[TEST] ${post.title}`,
      html,
    });

    if (result.error) {
      console.error("Failed to send test email:", result.error);
      process.exit(1);
    }

    console.log(`Test email sent to ${testEmail}: "${post.title}"`);
    return;
  }

  const audienceId = process.env.RESEND_AUDIENCE_ID;

  if (!audienceId) {
    console.error("Missing RESEND_AUDIENCE_ID environment variable.");
    process.exit(1);
  }

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
  const sinceLast = args.includes("--since-last");
  const shouldUpdateTracker = args.includes("--update-tracker");
  const testFlag = args.indexOf("--test");
  const testEmail = testFlag !== -1 ? args[testFlag + 1] : null;
  const slugFlag = args.indexOf("--slug");
  const slug = slugFlag !== -1 ? args[slugFlag + 1] : null;

  const tracker = sinceLast ? readTracker() : null;

  if (sinceLast) {
    const newPosts = getPostsSince(tracker.lastSentDate);
    if (newPosts.length === 0) {
      console.log(`No new posts since ${tracker.lastSentDate}. Nothing to send.`);
      return;
    }
    console.log(`Found ${newPosts.length} new post(s) since ${tracker.lastSentDate}:`);
    newPosts.forEach((f) => console.log(`  - ${f}`));
  }

  const filename = findPost(slug);

  if (sinceLast && tracker.lastSentFile === filename) {
    console.log(`Post already sent: ${filename}. Skipping.`);
    return;
  }

  console.log(`Processing: ${filename}`);

  const post = parsePost(filename);
  const { html, generatedFiles } = await renderEmail(post);

  if (generatedFiles.length > 0) {
    console.log(`Generated ${generatedFiles.length} PNG(s) in assets/email/`);
  }

  await sendNewsletter(html, post, { dryRun, testEmail });

  if (shouldUpdateTracker && !dryRun) {
    updateTracker(filename);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
