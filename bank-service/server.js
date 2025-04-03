const express = require('express');
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');
const sqlite3 = require('sqlite3').verbose();

// Initialize SQLite database
const db = new sqlite3.Database(':memory:'); 

// Create a table for customers
db.serialize(() => {
  db.run(`
    CREATE TABLE customers (
      id TEXT PRIMARY KEY,
      balance REAL
    )
  `);

  // Insert some sample data
  db.run("INSERT INTO customers (id, balance) VALUES ('C1001', 100)");
  db.run("INSERT INTO customers (id, balance) VALUES ('C1002', 200)");
  db.run("INSERT INTO customers (id, balance) VALUES ('C1003', 200)");
});

// Define GraphQL schema
const schema = buildSchema(`
  scalar JSON

  type Query {
    check(data: JSON): Boolean
  }

  type Mutation {
    addAmountToCustomer(id: String!, amount: Float!): Customer
  }

  type Customer {
    id: String
    balance: Float
  }
`);

// Define resolvers
const root = {
  // Resolver for /check
  check: ({ data }) => {
    // Simple validation logic: Check if the data is "valid"
    return true
  },

  // Resolver for /customer/id
  addAmountToCustomer: ({ id, amount }) => {
    return new Promise((resolve, reject) => {
      // Update the customer's balance in the database
      db.run(
        "UPDATE customers SET balance = balance + ? WHERE id = ?",
        [amount, id],
        function (err) {
          if (err) {
            reject(err);
          } else {
            // Fetch the updated customer record
            db.get(
              "SELECT * FROM customers WHERE id = ?",
              [id],
              (err, row) => {
                if (err) {
                  reject(err);
                } else {
                  resolve(row);
                }
              }
            );
          }
        }
      );
    });
  },
};

// Create Express app
const app = express();

// GraphQL endpoint for /check
app.use('/check', graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: true, // Enable GraphiQL interface for testing
}));

// GraphQL endpoint for /customer/id
app.use('/customer/id', graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: true, // Enable GraphiQL interface for testing
}));

// Start the server
const PORT = 4000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});