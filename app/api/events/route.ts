import {NextResponse} from "next/server";
const allowed=new Set(["diagnostic_started","diagnostic_completed","lesson_opened","practice_checked","reassessment_started"]);
export async function POST(request:Request){
 try{
  const body=await request.json();
  if(!body||typeof body.event!=="string"||!allowed.has(body.event)) return NextResponse.json({accepted:false},{status:400});
  const rawUrl=process.env.SUPABASE_URL;
 const trimmedUrl=rawUrl?.endsWith("/")?rawUrl.slice(0,-1):rawUrl;
 const url=trimmedUrl?.endsWith("/rest/v1")?trimmedUrl.slice(0,-8):trimmedUrl;
  const key=process.env.SUPABASE_SECRET_KEY;
  if(!url||!key){console.error("Analytics storage is not configured");return NextResponse.json({accepted:false},{status:503});}
  const row={event_type:body.event,skill:typeof body.skill==="string"?body.skill.slice(0,40):null};
  const response=await fetch(url+"/rest/v1/learning_events",{method:"POST",headers:{apikey:key,Authorization:"Bearer "+key,"Content-Type":"application/json",Prefer:"return=minimal"},body:JSON.stringify(row),cache:"no-store"});
  if(!response.ok){console.error("Analytics insert failed",response.status);return NextResponse.json({accepted:false},{status:502});}
  return NextResponse.json({accepted:true});
 }catch{return NextResponse.json({accepted:false},{status:400});}
}
