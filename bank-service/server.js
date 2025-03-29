const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');

 // Define your GraphQL schema
 const schema = buildSchema(`
    type Query {
      hello: String
    }
  `);

   // Define resolvers
 const root = {
    hello: () => 'Hello, GraphQL!'
  };

   // Create an Express app
 const app = express();

  // Create a route for handling GraphQL requests
  app.use('/graphql', graphqlHTTP({
    schema: schema,
    rootValue: root,
    graphiql: true // Enable GraphiQL for easy testing
  }));

   // Start the server
 const PORT = 3000;
 app.listen(PORT, () => {
   console.log(`Server is running at http://localhost:${PORT}/graphql`);
 });

 