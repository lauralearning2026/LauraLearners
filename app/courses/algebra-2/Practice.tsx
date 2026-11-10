"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import bank from "../../../lib/courses/algebra-2.json";
import styles from "./practice.module.css";

type Item = {
  id: string;
  category: string;
  standard: string;
  type: string;
  dok: number;
  calculator: string;
  stem: string;
  choices: string[];
  answer: number[];
  explanation: string;
  rationales: string[];
};
type Result = { id: string; category: string; right: boolean };

const items = bank.items as Item[];
const LETTERS = "ABCDEF";
const CATS: [string, string][] = [
  ["ALL", "All categories"],
  ["SO", "Structure & Operations"],
  ["EI", "Equations & Inequalities"],
  ["FN", "Functions"],
  ["SP", "Statistics & Probability"],
];
const catName = (k: string) => CATS.find(c => c[0] === k)?.[1] ?? k;

const KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/";
type RenderFn = (el: HTMLElement, opts: object) => void;

function useKatex(): boolean {
  const [ready, setReady] = useState(false);
  useEffect(() => {
    const w = window as unknown as { renderMathInElement?: RenderFn };
    if (w.renderMathInElement) { setReady(true); return; }
    if (!document.getElementById("katex-css")) {
      const link = document.createElement("link");
      link.id = "katex-css";
      link.rel = "stylesheet";
      link.href = KATEX + "katex.min.css";
      document.head.appendChild(link);
    }
    const load = (src: string) =>
      new Promise<void>((resolve, reject) => {
        const s = document.createElement("script");
        s.src = src;
        s.onload = () => resolve();
        s.onerror = () => reject(new Error(src));
        document.head.appendChild(s);
      });
    load(KATEX + "katex.min.js")
      .then(() => load(KATEX + "contrib/auto-render.min.js"))
      .then(() => setReady(true))
      .catch(() => setReady(false));
  }, []);
  return ready;
}

export default function Practice() {
  const [filter, setFilter] = useState("ALL");
  const [idx, setIdx] = useState(0);
  const [selected, setSelected] = useState<number[]>([]);
  const [checked, setChecked] = useState(false);
  const [results, setResults] = useState<Result[]>([]);
  const ready = useKatex();
  const box = useRef<HTMLDivElement>(null);

  const queue = useMemo(() => items.filter(q => filter === "ALL" || q.category === filter), [filter]);
  const q: Item | undefined = queue[idx];
  const done = idx >= queue.length;

  useEffect(() => {
    const w = window as unknown as { renderMathInElement?: RenderFn };
    if (ready && box.current && w.renderMathInElement) {
      w.renderMathInElement(box.current, {
        delimiters: [{ left: "\\(", right: "\\)", display: false }],
        throwOnError: false,
      });
    }
  }, [ready, idx, checked, filter, done]);

  function restart(next = filter) {
    setFilter(next);
    setIdx(0);
    setSelected([]);
    setChecked(false);
    setResults([]);
  }

  function pick(i: number) {
    if (checked || !q) return;
    if (q.type === "MC") setSelected([i]);
    else setSelected(s => (s.includes(i) ? s.filter(x => x !== i) : [...s, i]));
  }

  function check() {
    if (!q) return;
    const right = q.answer.length === selected.length && q.answer.every(a => selected.includes(a));
    setResults(r => [...r, { id: q.id, category: q.category, right }]);
    setChecked(true);
  }

  function next() {
    setIdx(i => i + 1);
    setSelected([]);
    setChecked(false);
  }

  const lastRight = results.length > 0 ? results[results.length - 1].right : false;

  return (
    <div ref={box}>
      <div className={styles.filters} role="group" aria-label="Reporting category">
        {CATS.map(([k, label]) => (
          <button key={k} aria-pressed={filter === k} onClick={() => restart(k)}>{label}</button>
        ))}
      </div>

      <div className={styles.progress}>{done ? "Results" : `Question ${idx + 1} of ${queue.length}`}</div>
      <div className={styles.bar}><span style={{ width: `${(Math.min(idx, queue.length) / queue.length) * 100}%` }} /></div>

      {!done && q ? (
        <section className={styles.card} key={q.id}>
          <div className={styles.meta}>
            <span>{catName(q.category)}</span>
            <span>{q.standard}</span>
            <span>DOK {q.dok}</span>
            <span>{q.calculator === "N" ? "No calculator" : "Calculator allowed"}</span>
            {q.type === "MS" && <span>Select all that apply</span>}
          </div>
          <div className={styles.stem} dangerouslySetInnerHTML={{ __html: q.stem }} />
          <div className={styles.choices}>
            {q.choices.map((c, i) => {
              const isAns = q.answer.includes(i);
              const isSel = selected.includes(i);
              const state = checked ? (isAns ? styles.correct : isSel ? styles.wrong : "") : "";
              return (
                <button
                  key={i}
                  className={`${styles.choice} ${state}`}
                  aria-pressed={isSel}
                  disabled={checked}
                  onClick={() => pick(i)}
                >
                  <b>{LETTERS[i]}.</b>
                  <span>
                    <span dangerouslySetInnerHTML={{ __html: c }} />
                    {checked && (isAns || isSel) && (
                      <span className={styles.why} dangerouslySetInnerHTML={{ __html: q.rationales[i] }} />
                    )}
                  </span>
                </button>
              );
            })}
          </div>
          {checked && (
            <div className={`feedback ${lastRight ? "good" : ""} ${styles.fb}`}>
              <strong>{lastRight ? "Correct." : "Not quite."}</strong>{" "}
              <span dangerouslySetInnerHTML={{ __html: q.explanation }} />
            </div>
          )}
          <div className={styles.actions}>
            {checked ? (
              <button className="submit" onClick={next}>{idx + 1 < queue.length ? "Next question →" : "See results →"}</button>
            ) : (
              <button className="submit" disabled={selected.length === 0} onClick={check}>Check answer</button>
            )}
          </div>
        </section>
      ) : (
        <section className="practiceResult">
          <small>YOUR RESULTS</small>
          <h2>{results.filter(r => r.right).length} of {results.length} correct</h2>
          <table className={styles.summary}>
            <thead><tr><th>Category</th><th>Score</th><th>Status</th></tr></thead>
            <tbody>
              {CATS.slice(1).map(([k, label]) => {
                const rs = results.filter(r => r.category === k);
                if (!rs.length) return null;
                const c = rs.filter(r => r.right).length;
                const pct = c / rs.length;
                return (
                  <tr key={k}>
                    <td>{label}</td>
                    <td>{c} / {rs.length}</td>
                    <td>{pct >= 0.8 ? "On track" : pct >= 0.5 ? "Keep practicing" : "Focus area"}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <button className="submit" onClick={() => restart()}>Try again</button>
        </section>
      )}
    </div>
  );
}
