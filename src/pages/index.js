// Step 1: Import React
import * as React from 'react'
import Layout from '../components/layout'
import { StaticImage } from 'gatsby-plugin-image'
// Step 2: Define your component
const IndexPage = () => {
  return (
    <Layout pageTitle="">
      <StaticImage
        alt="Playing With Quicksilver"
        src="../images/iStock-123202811.jpg"
        width={640}
        height={480}
      />
      <p>Computing is the mind at play. Let's explore that!</p>
    </Layout>
  )
}
// Step 3: Export your component
export default IndexPage