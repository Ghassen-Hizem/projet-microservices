package root.finrisk.service;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

/**
 * SOAP Web Service for retrieving customer financial profile activity
 * for risk assessment purposes.
 */
public class CustomerFinancialProfileService {

    private Connection dbConnection;

    /**
     * Constructor - initializes the in-memory SQLite database
     */
    public CustomerFinancialProfileService() {
        initializeDatabase();
        populateSampleData();
    }

    /**
     * Service method that will be exposed as a SOAP operation
     *
     * @param customerId The ID of the customer to retrieve financial profile for
     * @return CustomerFinancialProfile containing the customer's financial activities
     */
    public CustomerFinancialProfile getCustomerFinancialProfile(String customerId) {
        CustomerFinancialProfile profile = new CustomerFinancialProfile();
        profile.setCustomerId(customerId);

        try {
            // Get basic customer info
            String customerQuery = "SELECT * FROM customers WHERE customer_id = ?";
            PreparedStatement pstmt = dbConnection.prepareStatement(customerQuery);
            pstmt.setString(1, customerId);
            ResultSet rs = pstmt.executeQuery();

            if (rs.next()) {
                profile.setCustomerName(rs.getString("name"));
                profile.setAccountAge(rs.getInt("account_age_months"));
                profile.setCreditScore(rs.getInt("credit_score"));
            } else {
                return null; // Customer not found
            }

            // Get transaction history
            String transactionQuery = "SELECT * FROM transactions WHERE customer_id = ?";
            pstmt = dbConnection.prepareStatement(transactionQuery);
            pstmt.setString(1, customerId);
            rs = pstmt.executeQuery();

            List<Transaction> transactions = new ArrayList<>();
            while (rs.next()) {
                Transaction transaction = new Transaction();
                transaction.setTransactionId(rs.getString("transaction_id"));
                transaction.setAmount(rs.getDouble("amount"));
                transaction.setType(rs.getString("type"));
                transaction.setTimestamp(rs.getString("timestamp"));
                transaction.setCountry(rs.getString("country"));
                transactions.add(transaction);
            }
            profile.setTransactions(transactions);

            // Get suspicious activity flags
            String flagsQuery = "SELECT * FROM suspicious_activities WHERE customer_id = ?";
            pstmt = dbConnection.prepareStatement(flagsQuery);
            pstmt.setString(1, customerId);
            rs = pstmt.executeQuery();

            List<SuspiciousActivity> flags = new ArrayList<>();
            while (rs.next()) {
                SuspiciousActivity flag = new SuspiciousActivity();
                flag.setActivityId(rs.getString("activity_id"));
                flag.setActivityType(rs.getString("activity_type"));
                flag.setSeverity(rs.getInt("severity"));
                flag.setDescription(rs.getString("description"));
                flag.setTimestamp(rs.getString("timestamp"));
                flags.add(flag);
            }
            profile.setSuspiciousActivities(flags);

            return profile;

        } catch (SQLException e) {
            e.printStackTrace();
            return null;
        }
    }

    /**
     * Initialize the in-memory SQLite database and create necessary tables
     */
    private void initializeDatabase() {
        try {
            // Load the SQLite JDBC driver
            Class.forName("org.sqlite.JDBC");

            // Create an in-memory database
            dbConnection = DriverManager.getConnection("jdbc:sqlite::memory:");

            Statement stmt = dbConnection.createStatement();

            // Create customers table
            stmt.execute("CREATE TABLE customers (" +
                    "customer_id TEXT PRIMARY KEY, " +
                    "name TEXT, " +
                    "account_age_months INTEGER, " +
                    "credit_score INTEGER)");

            // Create transactions table
            stmt.execute("CREATE TABLE transactions (" +
                    "transaction_id TEXT PRIMARY KEY, " +
                    "customer_id TEXT, " +
                    "amount REAL, " +
                    "type TEXT, " +
                    "timestamp TEXT, " +
                    "country TEXT, " +
                    "FOREIGN KEY (customer_id) REFERENCES customers(customer_id))");

            // Create suspicious activities table
            stmt.execute("CREATE TABLE suspicious_activities (" +
                    "activity_id TEXT PRIMARY KEY, " +
                    "customer_id TEXT, " +
                    "activity_type TEXT, " +
                    "severity INTEGER, " +
                    "description TEXT, " +
                    "timestamp TEXT, " +
                    "FOREIGN KEY (customer_id) REFERENCES customers(customer_id))");

        } catch (ClassNotFoundException | SQLException e) {
            e.printStackTrace();
        }
    }

    /**
     * Populate the database with sample data for testing
     */
    private void populateSampleData() {
        try {
            Statement stmt = dbConnection.createStatement();

            // Insert sample customers
            stmt.execute("INSERT INTO customers VALUES " +
                    "('C1001', 'John Smith', 36, 720), " +
                    "('C1002', 'Jane Doe', 24, 680), " +
                    "('C1003', 'Bob Johnson', 6, 590)");

            // Insert sample transactions
            stmt.execute("INSERT INTO transactions VALUES " +
                    "('T1001', 'C1001', 5000.00, 'DEPOSIT', '2023-01-15 09:30:00', 'USA'), " +
                    "('T1002', 'C1001', 1200.00, 'WITHDRAWAL', '2023-01-20 14:45:00', 'USA'), " +
                    "('T1003', 'C1001', 3500.00, 'TRANSFER', '2023-02-05 11:15:00', 'CANADA'), " +
                    "('T1004', 'C1002', 2500.00, 'DEPOSIT', '2023-01-10 10:00:00', 'USA'), " +
                    "('T1005', 'C1002', 15000.00, 'DEPOSIT', '2023-02-01 16:30:00', 'MEXICO'), " +
                    "('T1006', 'C1003', 700.00, 'WITHDRAWAL', '2023-01-25 13:20:00', 'USA')");

            // Insert sample suspicious activities
            stmt.execute("INSERT INTO suspicious_activities VALUES " +
                    "('A1001', 'C1001', 'FOREIGN_TRANSFER', 2, 'Unusual transfer to foreign country', '2023-02-05 11:15:00'), " +
                    "('A1002', 'C1002', 'LARGE_DEPOSIT', 3, 'Unusually large deposit', '2023-02-01 16:30:00'), " +
                    "('A1003', 'C1002', 'FOREIGN_ACTIVITY', 1, 'Activity from foreign IP', '2023-02-01 16:30:00')");

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}