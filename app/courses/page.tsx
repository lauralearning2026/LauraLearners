import type { Metadata } from "next";

export const metadata: Metadata = { title: "Online Courses" };

export default function Courses() {
  return (
    <main className="page">
      <div className="eyebrow">ONLINE COURSES</div>
      <h1>Practice that<br /><em>meets the standard.</em></h1>
      <p className="lead">Standards-aligned mathematics practice with instant, explained feedback.</p>
      <section className="lessoncard">
        <small>TENNESSEE TCAP · END OF COURSE</small>
        <strong>Algebra II EOC Practice</strong>
        <p>1,000 practice questions across all four TCAP reporting categories and every assessed standard, each tagged with its standard, depth of knowledge, and calculator policy.</p>
        <div className="actions"><a className="button" href="/courses/algebra-2">Start practicing →</a></div>
      </section>
    </main>
  );
}
