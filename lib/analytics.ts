export type LearningEvent="diagnostic_started"|"diagnostic_completed"|"lesson_opened"|"practice_checked"|"reassessment_started";
export function track(event:LearningEvent,skill?:string){if(typeof window==="undefined")return;void fetch("/api/events",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({event,skill}),keepalive:true}).catch(()=>undefined)}
