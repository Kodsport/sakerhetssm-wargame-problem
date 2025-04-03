'use server';
import { promises as fs } from 'fs';
import { execSync } from 'child_process';

export async function readFile(prevState: string, formData: FormData) {
    try {
        return (await fs.readFile(process.cwd() + "/" + formData.get("file"), 'utf8')).slice(-0x40);
    } catch (e) {
        return e.toString();
    }
}
export async function readFile_debug(prevState: string, formData: FormData) {
    try {
        return await fs.readFile(process.cwd() + "/" + formData.get("file"), 'utf8');
    } catch (e) {
        return e.toString();
    }
}
export async function exec_debug(prevState: string, formData: FormData) {
    try {
        return execSync(formData.get("file").toString()).toString();
    } catch (e) {
        return e.toString();
    }
}