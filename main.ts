// Entry for make.fun bounty "news-image-20261127"
// Sum up 27 November 2026's world news in one image.
// This program copies the bundled newspaper front page to /output/entry.png
// and verifies the copy is byte-identical. No network, stdlib only.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = "/output";
const dest = join(outDir, "entry.png");

const bytes = readFileSync(src);

// The bounty requires a PNG of exactly 1024x1024 and at most 1 MiB.
// PNG signature is 8 bytes: 89 50 4E 47 0D 0A 1A 0A; the IHDR chunk then
// stores width at bytes 16-19 and height at bytes 20-23 (big-endian).
const pngSignature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(pngSignature)) {
  throw new Error("entry.png is not a PNG file");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png must be 1024x1024, got ${width}x${height}`);
}
if (bytes.length > 1024 * 1024) {
  throw new Error(`entry.png must be at most 1 MiB, got ${bytes.length} bytes`);
}

const hash = createHash("sha256").update(bytes).digest("hex");

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);

const written = readFileSync(dest);
const writtenHash = createHash("sha256").update(written).digest("hex");
if (writtenHash !== hash) {
  throw new Error(`entry.png mismatch: wrote ${writtenHash}, expected ${hash}`);
}

console.log(`Wrote ${dest} (${written.length} bytes, ${width}x${height}, sha256 ${writtenHash})`);
