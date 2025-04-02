package root.finrisk.service;

import java.util.List;

/**
 * Data class representing a customer's financial profile
 */
public class CustomerFinancialProfile {
    private String customerId;
    private String customerName;
    private int accountAge;
    private int creditScore;
    private List<Transaction> transactions;
    private List<SuspiciousActivity> suspiciousActivities;

    // Getters and setters
    public String getCustomerId() {
        return customerId;
    }

    public void setCustomerId(String customerId) {
        this.customerId = customerId;
    }

    public String getCustomerName() {
        return customerName;
    }

    public void setCustomerName(String customerName) {
        this.customerName = customerName;
    }

    public int getAccountAge() {
        return accountAge;
    }

    public void setAccountAge(int accountAge) {
        this.accountAge = accountAge;
    }

    public int getCreditScore() {
        return creditScore;
    }

    public void setCreditScore(int creditScore) {
        this.creditScore = creditScore;
    }

    public List<Transaction> getTransactions() {
        return transactions;
    }

    public void setTransactions(List<Transaction> transactions) {
        this.transactions = transactions;
    }

    public List<SuspiciousActivity> getSuspiciousActivities() {
        return suspiciousActivities;
    }

    public void setSuspiciousActivities(List<SuspiciousActivity> suspiciousActivities) {
        this.suspiciousActivities = suspiciousActivities;
    }
}
