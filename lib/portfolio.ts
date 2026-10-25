export type Project = { title: string; tag: string; summary: string; href?: string };

export const projects: Project[] = [
  { title: "Mathematics Teacher Support", tag: "Product Design · Learning Technology", summary: "An open-source teacher-support preview with mathematical explanations, lesson preparation, and short professional learning modules.", href: "/learn" },
  { title: "AI-Assisted Assessment Design", tag: "Professional Development · Generative AI", summary: "A teacher-learning experience focused on designing rigorous, standards-aligned assessment items with responsible AI." },
  { title: "Teacher Support Evaluation", tag: "Research · Evaluation Planning", summary: "A planned teacher-only pilot examining knowledge, confidence, and usability without student records.", href: "/impact" },
];

export type Category = {
  slug: string;
  name: string;
  description: string;
  icon: string;
  artifacts: number[];
  planned: string[];
};

export const categories: Category[] = [
  { slug: "curriculum-design", name: "Curriculum Design", icon: "🗺️", description: "Course maps, curriculum sequences, and standards-aligned plans.", artifacts: [], planned: ["Course map", "Unit sequence", "Standards alignment plan"] },
  { slug: "learning-design-activities", name: "Learning Design Activities", icon: "🧩", description: "Learning activities, assessments, and professional development.", artifacts: [1], planned: ["Learning activity design", "Assessment plan", "Professional development session"] },
  { slug: "instructional-media", name: "Instructional Media", icon: "🎬", description: "Infographics, storyboards, podcasts, and multimedia.", artifacts: [], planned: ["Infographic", "Storyboard", "Podcast or video"] },
  { slug: "quality-assurance-and-evaluation", name: "Quality Assurance and Evaluation", icon: "✅", description: "Quality assurance tools and evaluation plans.", artifacts: [2], planned: ["Quality review checklist", "Evaluation plan", "Course review report"] },
  { slug: "online-courses", name: "Online Courses", icon: "💻", description: "Documented online courses and their learning activities.", artifacts: [], planned: ["Online course module", "Course walkthrough", "Learner-facing activities"] },
];
