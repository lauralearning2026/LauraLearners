import type { Metadata } from "next";

export const metadata: Metadata = { title: "Contact Me" };

const reasons = [
  ["Instructional design", "Collaborating on course design, learning activities, or assessment."],
  ["Teacher support", "Trying LauraLearning with mathematics teachers in your school or program."],
  ["Open source", "Contributing content, feedback, or code to LauraLearning."],
];

export default function Contact() {
  return (
    <main className="page compactPage">
      <div className="eyebrow">CONTACT ME</div>
      <h1>Let's talk about <em>learning design.</em></h1>
      <p className="lead">I welcome conversations with fellow educators, instructional designers, and anyone interested in practical support for teaching mathematics.</p>

      <h2>I'd love to hear from you about</h2>
      <ul className="aboutList">
        {reasons.map(([title, text]) => <li key={title}><strong>{title}:</strong> {text}</li>)}
      </ul>

      <section className="contactCard">
        <small>EMAIL</small>
        <a href="mailto:Bkosgey6@gmail.com">Bkosgey6@gmail.com</a>
      </section>

      <div className="actions">
        <a className="button" href="mailto:Bkosgey6@gmail.com">Send me an email →</a>
        <a className="button secondary" href="/resume">View my resume</a>
      </div>
    </main>
  );
}
