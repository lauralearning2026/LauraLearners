import { createHash, createHmac, randomInt, timingSafeEqual } from "node:crypto";
import { q } from "./db";

export type Role = "teacher" | "admin" | "student";
export type User = { id: number; role: Role; label: string; class_id: number | null; code: string };

const COOKIE = "a2p_session";
const MAX_AGE = 60 * 60 * 24 * 120; // about one semester
const ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"; // no 0/O, 1/I/L

function secret(): string {
  if (process.env.SESSION_SECRET) return process.env.SESSION_SECRET;
  const db = process.env.DATABASE_URL || process.env.POSTGRES_URL || "";
  return createHash("sha256").update("a2p-session|" + db).digest("hex");
}

function sign(value: string): string {
  return createHmac("sha256", secret()).update(value).digest("base64url");
}

export function newCode(): string {
  let s = "";
  for (let i = 0; i < 8; i++) s += ALPHABET[randomInt(ALPHABET.length)];
  return s;
}

/** Codes are typed by students: ignore case, spaces and dashes. */
export function normalizeCode(input: string): string {
  return String(input || "").toUpperCase().replace(/[^A-Z0-9]/g, "");
}

export function formatCode(code: string): string {
  return code.length === 8 ? `${code.slice(0, 4)}-${code.slice(4)}` : code;
}

export function sessionCookie(userId: number, req: Request): string {
  const value = `${userId}.${Date.now()}`;
  const secure = new URL(req.url).protocol === "https:" ? "; Secure" : "";
  return `${COOKIE}=${value}.${sign(value)}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${MAX_AGE}${secure}`;
}

export function clearCookie(): string {
  return `${COOKIE}=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0`;
}

function readCookie(req: Request): string | null {
  const raw = req.headers.get("cookie") || "";
  for (const part of raw.split(";")) {
    const [k, ...v] = part.trim().split("=");
    if (k === COOKIE) return v.join("=");
  }
  return null;
}

/** The signed-in user, or null. Deactivated users are signed out immediately. */
export async function currentUser(req: Request): Promise<User | null> {
  const c = readCookie(req);
  if (!c) return null;
  const parts = c.split(".");
  if (parts.length !== 3) return null;
  const [id, ts, mac] = parts;
  const expected = sign(`${id}.${ts}`);
  const a = Buffer.from(mac), b = Buffer.from(expected);
  if (a.length !== b.length || !timingSafeEqual(a, b)) return null;
  if (Date.now() - Number(ts) > MAX_AGE * 1000) return null;
  const rows = await q<User>(
    `UPDATE users SET last_seen = now() WHERE id = $1::int AND active RETURNING id, role, label, class_id, code`,
    [Number(id)],
  );
  return rows[0] || null;
}
