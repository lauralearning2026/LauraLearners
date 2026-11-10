import type { Metadata } from "next";
import Practice from "./Practice";

export const metadata: Metadata = {
  title: "Algebra II EOC Practice",
  description: "Standards-aligned Algebra II practice for the Tennessee TCAP end-of-course exam, with instant feedback.",
};

export default function Algebra2Practice() {
  return (
    <main className="page">
      <div className="eyebrow">ONLINE COURSES · ALGEBRA II</div>
      <h1>Algebra II<br /><em>EOC practice.</em></h1>
      <p className="lead">
        Practice aligned to the 2023–24 Tennessee Algebra II standards and the TCAP blueprint. Choose a reporting
        category, answer each question, and get instant feedback on every choice.
      </p>
      <Practice />
      <section className="lessoncard">
        <small>ABOUT THESE QUESTIONS</small>
        <p>
          These are original practice items written in the style of released TCAP items. They are not official TCAP
          questions. Answers are not saved or sent anywhere, and no account is required.
        </p>
      </section>
    </main>
  );
}
