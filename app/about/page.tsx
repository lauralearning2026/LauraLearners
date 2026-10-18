import type { Metadata } from "next";

export const metadata: Metadata = { title: "About Brigid Kosgey" };

export default function About() {
  return (
    <main className="page compactPage">
      <div className="eyebrow">ABOUT ME</div>
      <h1>Teaching shapes <em>my design.</em></h1>
      <p className="lead">I am Brigid Kosgey, an Algebra II teacher at a public high school in Memphis, Tennessee, now in my third year of teaching in the United States.</p>

      <h2>From classroom challenges to learning experiences</h2>
      <p>Many of my students reach Algebra II with gaps in foundational skills that began years earlier. Teaching them has shown me how much depends on the teacher's own explanation of why each step works, and how hard that is when a teacher is assigned mathematics outside their original preparation.</p>
      <p>That is the problem LauraLearning sets out to address: short, practical support that helps teachers understand the mathematics, anticipate student misconceptions, and prepare their next lesson.</p>

      <h2>Background</h2>
      <ul className="aboutList">
        <li><strong>Teaching:</strong> Algebra II at a public high school in Memphis, Tennessee, now in my third year.</li>
        <li><strong>Education:</strong> degree equivalent to a US bachelor's in mathematics education.</li>
        <li><strong>Graduate study:</strong> M.Ed. in Instructional Design and Educational Technology (in progress) at American College of Education, and graduate coursework in Applied Artificial Intelligence at Eastern University.</li>
        <li><strong>Open source:</strong> LauraLearning's code is free and openly licensed so schools and teachers can use and adapt it.</li>
      </ul>

      <div className="actions">
        <a className="button" href="/learn">Explore teacher support →</a>
        <a className="button secondary" href="/portfolio">View my portfolio</a>
      </div>
    </main>
  );
}
