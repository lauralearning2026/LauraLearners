import {NextResponse} from "next/server";
export async function POST(){return NextResponse.json({accepted:false,reason:"Application event collection is disabled during the teacher-support preview."},{status:410});}
