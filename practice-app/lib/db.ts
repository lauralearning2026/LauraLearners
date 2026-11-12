import { neon } from "@neondatabase/serverless";

type Row = Record<string, any>;
type Runner = (text: string, params?: unknown[]) => Promise<Row[]>;

let runner: Runner | null = null;
let ready: Promise<void> | null = null;

function connectionString(): string {
  const url = process.env.DATABASE_URL || process.env.POSTGRES_URL;
  if (!url) throw new Error("No database is connected. Add a Postgres database to this Vercel project.");
  return url;
}

function run(): Runner {
  if (!runner) runner = neon(connectionString()) as unknown as Runner;
  return runner;
}

const SCHEMA = [
  `CREATE TABLE IF NOT EXISTS classes (
     id serial PRIMARY KEY,
     name text NOT NULL,
     created_at timestamptz NOT NULL DEFAULT now())`,
  `CREATE TABLE IF NOT EXISTS users (
     id serial PRIMARY KEY,
     code text NOT NULL UNIQUE,
     role text NOT NULL CHECK (role IN ('teacher', 'admin', 'student')),
     label text NOT NULL DEFAULT '',
     class_id int REFERENCES classes(id) ON DELETE SET NULL,
     active boolean NOT NULL DEFAULT true,
     created_at timestamptz NOT NULL DEFAULT now(),
     last_seen timestamptz)`,
  `CREATE TABLE IF NOT EXISTS assignments (
     id serial PRIMARY KEY,
     class_id int NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
     standard text NOT NULL,
     item_ids text[] NOT NULL,
     user_ids int[] NOT NULL,
     note text NOT NULL DEFAULT '',
     closed boolean NOT NULL DEFAULT false,
     created_at timestamptz NOT NULL DEFAULT now())`,
  `CREATE TABLE IF NOT EXISTS answers (
     id serial PRIMARY KEY,
     user_id int NOT NULL REFERENCES users(id) ON DELETE CASCADE,
     item_id text NOT NULL,
     standard text NOT NULL,
     correct boolean NOT NULL,
     picked int[] NOT NULL,
     err text,
     assignment_id int REFERENCES assignments(id) ON DELETE SET NULL,
     answered_at timestamptz NOT NULL DEFAULT now())`,
  `CREATE INDEX IF NOT EXISTS answers_user_idx ON answers (user_id)`,
  `CREATE TABLE IF NOT EXISTS dismissed (
     class_id int NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
     standard text NOT NULL,
     created_at timestamptz NOT NULL DEFAULT now(),
     PRIMARY KEY (class_id, standard))`,
  `CREATE TABLE IF NOT EXISTS settings (
     key text PRIMARY KEY,
     value jsonb NOT NULL)`,
];

async function ensureSchema(): Promise<void> {
  const r = run();
  for (const stmt of SCHEMA) await r(stmt, []);
}

/** Run one SQL statement with $1, $2 … parameters. Creates the tables on first use. */
export async function q<T extends Row = Row>(text: string, params: unknown[] = []): Promise<T[]> {
  if (!ready) ready = ensureSchema().catch(e => { ready = null; throw e; });
  await ready;
  return (await run()(text, params)) as T[];
}

/** The school's local day for an answer, so "this week" matches the classroom calendar. */
export const LOCAL_DAY = `to_char(answered_at AT TIME ZONE 'America/Chicago', 'YYYY-MM-DD')`;
