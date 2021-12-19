// Step 1: Import React
import * as React from 'react'
import Layout from '../components/layout'
import { StaticImage } from 'gatsby-plugin-image'
// Step 2: Define your component
const IndexPage = () => {
  return (
    <Layout pageTitle="">
      <p>Computing is the mind at play. Let's explore that!</p>
      <StaticImage
        alt="Playing With Quicksilver"
        src="../images/iStock-123202811.jpg"
      />
    </Layout>
  )
}
// Step 3: Export your component
export default IndexPage