import {NextResponse} from "next/server";
export async function GET(){return NextResponse.json({status:"ok",mode:"teacher-support-preview",eventCollectionEnabled:false,databaseRequired:false});}
