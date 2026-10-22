import type { Metadata } from "next";
import { existsSync } from "fs";
import { join } from "path";

export const metadata: Metadata = { title: "Design Philosophy" };

const principles = [
  ["Start from prior knowledge", "New ideas need somewhere to attach. Design begins by finding out what learners already understand and where the gaps are."],
  ["Model the thinking, not just the steps", "Clear worked examples make the reasoning visible, so learners see why a step works and not only what to do."],
  ["Release responsibility gradually", "Learning moves from modeling, to guided practice, to independent work, with support reduced as understanding grows."],
  ["Use feedback to choose the next step", "Assessment is most useful when it tells the learner and the teacher what to do next."],
  ["Let technology serve the design", "Tools should support these decisions rather than determine them."],
];

export default function Philosophy() {
  const hasToolkit = existsSync(join(process.cwd(), "public", "learning-design-toolkit.pdf"));
  return (
    <main className="page compactPage">
      <div className="eyebrow">PHILOSOPHY OF LEARNING DESIGN AND TECHNOLOGY</div>
      <h1>Design for <em>understanding.</em></h1>
      <p className="lead">Learning design should make important ideas accessible without hiding the thinking learners need to do.</p>

      <h2>Five principles</h2>
      <ol className="principles">
        {principles.map(([title, text]) => (
          <li key={title}><strong>{title}</strong><p>{text}</p></li>
        ))}
      </ol>

      <h2>In practice</h2>
      <p>In my Algebra II classroom, many learners need support with foundational equations and functions before tackling more advanced concepts. That makes careful sequencing and attention to cognitive load essential, and it shapes how LauraLearning supports teachers: understand the mathematics first, anticipate misconceptions, then prepare the lesson.</p>

      {hasToolkit && (
        <section className="toolkit">
          <h2>Learning Design Toolkit</h2>
          <p>My Learning Design Toolkit, developed in Fundamentals of Learning Design and Technology, gathers the learning theories, design and project management models, cognitive load principles, learning strategies, and learner analysis tools that guide my design decisions, each with an example from my Algebra II classroom.</p>
          <iframe src="/learning-design-toolkit.pdf#view=FitH" title="Learning Design Toolkit (PDF)" className="pdfFrame" />
          <a className="projectLink" href="/learning-design-toolkit.pdf" target="_blank" rel="noopener">Open the toolkit as a PDF →</a>
        </section>
      )}

      <div className="actions">
        <a className="button" href="/learn">See it in LauraLearning →</a>
        <a className="button secondary" href="/portfolio">View my portfolio</a>
      </div>
    </main>
  );
}
