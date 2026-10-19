import type { Metadata } from "next";
import { existsSync } from "fs";
import { join } from "path";

export const metadata: Metadata = { title: "Resume" };

const skills = [
  "Instructional design and lesson sequencing",
  "Standards-aligned assessment design",
  "Gradual release of responsibility",
  "Educational technology and web development (Next.js, Vercel)",
  "Cloud foundations (AWS) and data engineering coursework",
];

export default function Resume() {
  const hasPdf = existsSync(join(process.cwd(), "public", "resume.pdf"));
  return (
    <main className="page compactPage resumePage">
      <div className="eyebrow">RESUME</div>
      <h1>Brigid <em>Kosgey</em></h1>
      <p className="lead">Mathematics teacher and instructional designer building practical, classroom-grounded support for teachers of mathematics.</p>
      <p className="resumeContact">Memphis, Tennessee · <a href="mailto:Bkosgey6@gmail.com">Bkosgey6@gmail.com</a> · <a href="https://www.lauralearning.org">lauralearning.org</a></p>
      {hasPdf && <a className="button" href="/resume.pdf" download>Download resume (PDF)</a>}

      <h2>Experience</h2>
      <article className="resumeItem">
        <div><strong>Algebra II Teacher</strong><span>Public high school, Memphis, Tennessee · Third year, current</span></div>
        <ul>
          <li>Teach five sections of Algebra II, using the gradual release model to move students from modeling to independent work.</li>
          <li>Design scaffolds for students who arrive with gaps in foundational skills from earlier grades.</li>
        </ul>
      </article>
      <article className="resumeItem">
        <div><strong>Founder and Designer, LauraLearning</strong><span>Open-source project · 2026, current</span></div>
        <ul>
          <li>Designed and built an open-source teacher-support platform with a knowledge check, worked examples, lesson resources, and a short learning module.</li>
          <li>Planned a privacy-conscious, teacher-only pilot to evaluate knowledge, confidence, and usability.</li>
        </ul>
      </article>

      <h2>Education</h2>
      <article className="resumeItem">
        <div><strong>M.Ed., Instructional Design and Educational Technology</strong><span>American College of Education · In progress</span></div>
      </article>
      <article className="resumeItem">
        <div><strong>Graduate coursework, Applied Artificial Intelligence</strong><span>Eastern University · Coursework completed in Foundations of Machine Learning, Introduction to Artificial Intelligence, Cloud Foundations (AWS), and Data Engineering in the Cloud (AWS)</span></div>
      </article>
      <article className="resumeItem">
        <div><strong>Bachelor of Education, Mathematics Education</strong><span>Moi University, Kenya · 2006 · Evaluated as equivalent to a US bachelor's degree in education with a concentration in mathematics</span></div>
      </article>

      <h2>Skills</h2>
      <ul className="aboutList">{skills.map(s => <li key={s}>{s}</li>)}</ul>
    </main>
  );
}
