import {NextResponse} from "next/server";
export async function GET(){
 const rawUrl=process.env.SUPABASE_URL;
  const url=rawUrl?.replace(/\\/rest\\/v1\\/?$/, "").replace(/\\/$/, "");
 const key=process.env.SUPABASE_SECRET_KEY;
 if(!url||!key) return NextResponse.json({configured:false,databaseReachable:false},{status:503});
 try{
  const response=await fetch(url+"/rest/v1/learning_events?select=id&limit=1",{headers:{apikey:key,Authorization:"Bearer "+key},cache:"no-store"});
  return NextResponse.json({configured:true,databaseReachable:response.ok,status:response.status},{status:response.ok?200:502});
 }catch{return NextResponse.json({configured:true,databaseReachable:false},{status:502});}
}
