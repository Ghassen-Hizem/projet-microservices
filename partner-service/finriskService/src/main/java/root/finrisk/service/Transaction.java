package root.finrisk.service;

/**
 * Data class representing a financial transaction
 * This class contains details about a customer's banking transaction
 */
public class Transaction {
    private String transactionId;
    private String customerId;
    private double amount;
    private String type;
    private String timestamp;
    private String country;
    private String merchantCategory;
    private String status;
    private String currency;
    private String channel;

    /**
     * Default constructor
     */
    public Transaction() {
    }

    /**
     * Parameterized constructor
     *
     * @param transactionId Unique identifier for the transaction
     * @param customerId ID of the customer who performed the transaction
     * @param amount Transaction amount
     * @param type Type of transaction (DEPOSIT, WITHDRAWAL, TRANSFER, etc.)
     * @param timestamp Date/time when the transaction occurred
     * @param country Country where the transaction was initiated
     */
    public Transaction(String transactionId, String customerId, double amount,
                       String type, String timestamp, String country) {
        this.transactionId = transactionId;
        this.customerId = customerId;
        this.amount = amount;
        this.type = type;
        this.timestamp = timestamp;
        this.country = country;
    }

    // Getters and setters
    public String getTransactionId() {
        return transactionId;
    }

    public void setTransactionId(String transactionId) {
        this.transactionId = transactionId;
    }

    public String getCustomerId() {
        return customerId;
    }

    public void setCustomerId(String customerId) {
        this.customerId = customerId;
    }

    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public String getMerchantCategory() {
        return merchantCategory;
    }

    public void setMerchantCategory(String merchantCategory) {
        this.merchantCategory = merchantCategory;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getCurrency() {
        return currency;
    }

    public void setCurrency(String currency) {
        this.currency = currency;
    }

    public String getChannel() {
        return channel;
    }

    public void setChannel(String channel) {
        this.channel = channel;
    }

    @Override
    public String toString() {
        return "Transaction{" +
                "transactionId='" + transactionId + '\'' +
                ", customerId='" + customerId + '\'' +
                ", amount=" + amount +
                ", type='" + type + '\'' +
                ", timestamp='" + timestamp + '\'' +
                ", country='" + country + '\'' +
                ", merchantCategory='" + merchantCategory + '\'' +
                ", status='" + status + '\'' +
                ", currency='" + currency + '\'' +
                ", channel='" + channel + '\'' +
                '}';
    }
}