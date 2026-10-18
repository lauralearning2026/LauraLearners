import type { Metadata } from "next";

export const metadata: Metadata = { title: "Evaluation Status" };

export default function Analytics(){return <main className="page"><div className="eyebrow">EVALUATION STATUS</div><h1>No results yet.<br/><em>Reported when real.</em></h1><p className="lead">The teacher-support preview does not collect usage data, and no pilot has been completed yet.</p><section className="lessoncard"><h2>What will appear here</h2><p>Once a consent-based teacher pilot is complete, this page will report participation and pre/post results, with the methodology and limitations alongside them.</p><a href="/impact/methodology">Read the evaluation approach →</a></section></main>}