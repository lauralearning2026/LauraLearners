import type { Metadata } from "next";

export const metadata: Metadata = { title: "Instructional Design Portfolio" };

const projects = [
  ["Mathematics Teacher Support", "Product Design · Learning Technology", "An open-source teacher-support preview with mathematical explanations, lesson preparation, and short professional learning modules.", "/learn"],
  ["AI-Assisted Assessment Design", "Professional Development · Generative AI", "A teacher-learning experience focused on designing rigorous, standards-aligned assessment items with responsible AI.", ""],
  ["Teacher Support Evaluation", "Research · Evaluation Planning", "A planned teacher-only pilot examining knowledge, confidence, and usability without student records.", "/impact"],
];

const categories: { name: string; description: string; artifacts: number[] }[] = [
  { name: "Curriculum Design", description: "Course maps, curriculum sequences, and standards-aligned plans.", artifacts: [] },
  { name: "Learning Design Activities", description: "Learning activities, assessments, and professional development.", artifacts: [1] },
  { name: "Instructional Media", description: "Infographics, storyboards, podcasts, and multimedia.", artifacts: [] },
  { name: "Quality Assurance and Evaluation", description: "Quality assurance tools and evaluation plans.", artifacts: [2] },
  { name: "Online Courses", description: "Documented online courses and their learning activities.", artifacts: [] },
];

export default function Portfolio() {
  const filled = categories.map((c, i) => ({ ...c, i })).filter(c => c.artifacts.length);
  const upcoming = categories.map((c, i) => ({ ...c, i })).filter(c => !c.artifacts.length);
  return (
    <main className="page portfolioPage">
      <div className="eyebrow">INSTRUCTIONAL DESIGN PORTFOLIO</div>
      <h1>Problems worth solving.<br /><em>Products worth using.</em></h1>
      <p className="lead">A growing collection of learning experiences, systems, and research-informed design work.</p>

      <section className="portfolioExisting">
        <h2>Projects</h2>
        <div className="projects">
          {projects.map((p, i) => (
            <article key={p[0]}>
              <span>0{i + 1}</span>
              <div><small>{p[1]}</small><h2>{p[0]}</h2><p>{p[2]}</p>{p[3] && <a className="projectLink" href={p[3]}>View project →</a>}</div>
            </article>
          ))}
        </div>
      </section>

      <section className="portfolioCategories">
        <div className="eyebrow">ACE EPORTFOLIO CATEGORIES</div>
        <h2>Browse by area of practice</h2>
        <nav className="categoryJump" aria-label="Portfolio sections">
          {categories.map((c, i) => <a key={c.name} href={"#category-" + i}>{c.name}</a>)}
        </nav>
        {filled.map(category => (
          <article id={"category-" + category.i} key={category.name}>
            <div><span className="eyebrow">0{category.i + 1} / 05</span><h3>{category.name}</h3><p>{category.description}</p></div>
            <div>{category.artifacts.map(index => (
              <div className="portfolioArtifact" key={index}><strong>{projects[index][0]}</strong><p>{projects[index][2]}</p></div>
            ))}</div>
          </article>
        ))}
        <article className="upcoming">
          <div><span className="eyebrow">IN PROGRESS</span><h3>Coming with coursework</h3><p>Artifacts for these categories will be added as M.Ed. coursework is completed.</p></div>
          <ul>
            {upcoming.map(category => (
              <li id={"category-" + category.i} key={category.name}><strong>{category.name}</strong><span>{category.description}</span></li>
            ))}
          </ul>
        </article>
      </section>

      <section className="portfolioProjectLink">
        <h2>Explore LauraLearning</h2>
        <p>See the working mathematics teacher-support project.</p>
        <a className="button" href="/learn">Visit LauraLearning →</a>
      </section>
    </main>
  );
}
