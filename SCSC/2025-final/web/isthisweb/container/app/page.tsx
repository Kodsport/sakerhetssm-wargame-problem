'use client';
import { useActionState } from 'react';
import { readFile } from './actions';

export default function Page() {
  const [state, formAction] = useActionState(readFile,"");
  return <form action={formAction}>
    <input name="file" type="text" />
    <button type="submit">Read</button>
    {state}
  </form>
}