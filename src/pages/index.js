import * as React from 'react'
import Layout from '../components/layout'
import { StaticImage } from 'gatsby-plugin-image'

const IndexPage = () => {
  return (
    <Layout pageTitle="">
      <p>Computing is the mind at play. Let's explore that!</p>
      <StaticImage
        alt="Playing With Quicksilver"
        src="../images/iStock-123202811.jpg"
        width={640}
        height={480}
        loading="eager"
      />
    </Layout>
  )
}
// Step 3: Export your component
export default IndexPage