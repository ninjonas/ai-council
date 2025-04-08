import type { AppProps } from 'next/app'
import '../app/globals.css'
import '../styles/force-tailwind.css'

export default function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}
