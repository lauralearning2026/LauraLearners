// Legacy application event collection is disabled during the teacher-support pivot.
export type LearningEvent="diagnostic_started"|"diagnostic_completed"|"lesson_opened"|"practice_checked"|"reassessment_started";
export function track(_event:LearningEvent,_skill?:string):void {}
