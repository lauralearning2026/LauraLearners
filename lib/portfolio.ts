export type Project = { title: string; tag: string; summary: string; href?: string };

export const projects: Project[] = [
  { title: "Mathematics Teacher Support", tag: "Product Design · Learning Technology", summary: "An open-source teacher-support preview with mathematical explanations, lesson preparation, and short professional learning modules.", href: "/learn" },
  { title: "AI-Assisted Assessment Design", tag: "Professional Development · Generative AI", summary: "A teacher-learning experience focused on designing rigorous, standards-aligned assessment items with responsible AI." },
  { title: "Teacher Support Evaluation", tag: "Research · Evaluation Planning", summary: "A planned teacher-only pilot examining knowledge, confidence, and usability without student records.", href: "/impact" },
];

/** A program assignment that will become a portfolio artifact (from the ACE ePortfolio roadmap). */
export type Planned = { title: string; course: string; module: string; purpose: string };

export type Category = {
  slug: string;
  name: string;
  description: string;
  icon: string;
  artifacts: number[];
  planned: Planned[];
};

export const categories: Category[] = [
  {
    slug: "curriculum-design", name: "Curriculum Design", icon: "🗺️",
    description: "Course maps, curriculum sequences, and standards-aligned plans.", artifacts: [],
    planned: [
      { title: "Course Map", course: "TECH5213", module: "Module 5", purpose: "Visualize and organize a curriculum to show the full learning journey." },
    ],
  },
  {
    slug: "learning-design-activities", name: "Learning Design Activities", icon: "🧩",
    description: "Learning activities, assessments, and professional development.", artifacts: [1],
    planned: [
      { title: "Assessment", course: "TECH5233", module: "Module 4", purpose: "Design assessment strategies that evaluate learning outcomes." },
    ],
  },
  {
    slug: "instructional-media", name: "Instructional Media", icon: "🎬",
    description: "Infographics, storyboards, podcasts, and multimedia.", artifacts: [],
    planned: [
      { title: "Infographic", course: "TECH5233", module: "Module 3", purpose: "A visual resource that simplifies complex information." },
      { title: "Infographic", course: "TECH5243", module: "Module 2", purpose: "A visual resource that simplifies complex information." },
      { title: "Podcast", course: "TECH5243", module: "Module 3", purpose: "Engaging audio content for educational delivery." },
      { title: "Storyboard", course: "TECH5243", module: "Module 4", purpose: "A storyboard that plans the visual narrative of a multimedia project." },
      { title: "Branded Resource and Branding Template", course: "TECH5263", module: "Module 3", purpose: "A consistent professional brand identity across materials." },
      { title: "Animated Video", course: "TECH5263", module: "Module 5", purpose: "A high-quality animated video that showcases multimedia design skills." },
    ],
  },
  {
    slug: "quality-assurance-and-evaluation", name: "Quality Assurance and Evaluation", icon: "✅",
    description: "Quality assurance tools and evaluation plans.", artifacts: [2],
    planned: [
      { title: "QA Checklist Template", course: "TECH5223", module: "Module 5", purpose: "A professional quality assurance tool for content accuracy and consistency." },
      { title: "Decision Matrix", course: "TECH5253", module: "Module 3", purpose: "A decision-making framework for analyzing and selecting instructional solutions." },
    ],
  },
  {
    slug: "online-courses", name: "Online Courses", icon: "💻",
    description: "Documented online courses and their learning activities.", artifacts: [],
    planned: [
      { title: "Assembled LMS Course", course: "TECH5273", module: "Modules 4–5", purpose: "A course structure with learning and assessment components assembled in an LMS." },
    ],
  },
];

/** The nine steps of the ACE Instructional Design program ePortfolio roadmap. */
export const roadmap: { step: number; course: string; artifacts: string; purpose: string; done?: boolean; href?: string }[] = [
  { step: 1, course: "TECH5203", artifacts: "Initial Portfolio Website (Module 5)", purpose: "Establish the platform and structure for showcasing my work.", done: true, href: "/" },
  { step: 2, course: "TECH5213", artifacts: "Course Map (Module 5)", purpose: "Visualize and organize a curriculum.", href: "/portfolio/curriculum-design" },
  { step: 3, course: "TECH5223", artifacts: "QA Checklist Template (Module 5)", purpose: "Ensure content accuracy and consistency.", href: "/portfolio/quality-assurance-and-evaluation" },
  { step: 4, course: "TECH5233", artifacts: "Infographic (Module 3) · Assessment (Module 4)", purpose: "Simplify complex information and evaluate learning outcomes.", href: "/portfolio/instructional-media" },
  { step: 5, course: "TECH5243", artifacts: "Infographic (Module 2) · Podcast (Module 3) · Storyboard (Module 4)", purpose: "Visual, audio, and storyboarded multimedia.", href: "/portfolio/instructional-media" },
  { step: 6, course: "TECH5253", artifacts: "Decision Matrix (Module 3)", purpose: "Analyze and select instructional solutions.", href: "/portfolio/quality-assurance-and-evaluation" },
  { step: 7, course: "TECH5263", artifacts: "Branded Resource and Branding Template (Module 3) · Animated Video (Module 5)", purpose: "A professional brand and an animated video.", href: "/portfolio/instructional-media" },
  { step: 8, course: "TECH5273", artifacts: "Philosophy of Learning Design and Technology (Module 4) · Assembled LMS (Modules 4–5)", purpose: "My design philosophy and a complete LMS course.", href: "/philosophy" },
  { step: 9, course: "Capstone", artifacts: "Comprehensive ePortfolio", purpose: "Curate the artifacts that represent my best work, refined with faculty feedback." },
];
