export default function Layout({
  children,
}: {
  children: React.ReactNode
}) {
  return (  
    <html lang="en">
      <title>Is this web?</title>
      <body>
        <main>{children}</main>
      </body>
    </html>
  )
}