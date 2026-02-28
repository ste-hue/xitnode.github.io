const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const matter = require("gray-matter");
const { marked } = require("marked");

const POSTS_DIR = path.join(__dirname, "..", "_posts");
const TEMPLATE_PATH = path.join(__dirname, "email-template.html");
const OUTPUT_PATH = path.join(__dirname, "preview-output.html");
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
  const categories = Array.isArray(data.categories) ? data.categories : [];
  const categoryPath = categories.length > 0 ? categories.join("/") + "/" : "";
  const postUrl = `${SITE_URL}/${categoryPath}${yearMatch[1]}/${monthMatch[1]}/${dayMatch[1]}/${slugPart}`;

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
  // Replace unsubscribe placeholder with a dummy link for preview
  template = template.replace("{{{UNSUBSCRIBE_URL}}}", "#unsubscribe-preview");
  return template;
}

function main() {
  const slug = process.argv[2] || null;

  const filename = findPost(slug);
  console.log(`Previewing: ${filename}`);

  const post = parsePost(filename);
  const html = renderEmail(post);

  fs.writeFileSync(OUTPUT_PATH, html, "utf-8");
  console.log(`Written to: ${OUTPUT_PATH}`);

  try {
    execSync(`open "${OUTPUT_PATH}"`);
    console.log("Opened in browser.");
  } catch {
    console.log("Could not open browser automatically. Open the file manually.");
  }
}

main();
