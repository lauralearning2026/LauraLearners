import {NextResponse} from "next/server";
export async function GET(){
 const rawUrl=process.env.SUPABASE_URL;
 const trimmedUrl=rawUrl?.endsWith("/")?rawUrl.slice(0,-1):rawUrl;
 const url=trimmedUrl?.endsWith("/rest/v1")?trimmedUrl.slice(0,-8):trimmedUrl;
 const key=process.env.SUPABASE_SECRET_KEY;
 if(!url||!key) return NextResponse.json({configured:false,databaseReachable:false},{status:503});
 try{
  const response=await fetch(url+"/rest/v1/learning_events?select=id&limit=1",{headers:{apikey:key,Authorization:"Bearer "+key},cache:"no-store"});
  return NextResponse.json({configured:true,databaseReachable:response.ok,status:response.status},{status:response.ok?200:502});
 }catch{return NextResponse.json({configured:true,databaseReachable:false},{status:502});}
}
