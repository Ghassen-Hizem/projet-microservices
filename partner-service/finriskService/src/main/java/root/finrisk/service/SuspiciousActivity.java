package root.finrisk.service;

/**
 * Data class representing a suspicious activity flag in a customer's financial profile
 * This class contains details about activities that have been flagged as potentially suspicious
 */
public class SuspiciousActivity {
    private String activityId;
    private String customerId;
    private String activityType;
    private int severity;  // 1-5 scale where 5 is most severe
    private String description;
    private String timestamp;
    private String relatedTransactionId;
    private String detectionMethod;
    private boolean verified;
    private String resolutionStatus;

    /**
     * Default constructor
     */
    public SuspiciousActivity() {
    }

    /**
     * Parameterized constructor
     *
     * @param activityId Unique identifier for the suspicious activity
     * @param customerId ID of the customer associated with this activity
     * @param activityType Type of suspicious activity (e.g., FOREIGN_TRANSFER, LARGE_DEPOSIT)
     * @param severity Risk severity level (1-5)
     * @param description Human-readable description of the suspicious activity
     * @param timestamp Date/time when the activity was detected
     */
    public SuspiciousActivity(String activityId, String customerId, String activityType,
                              int severity, String description, String timestamp) {
        this.activityId = activityId;
        this.customerId = customerId;
        this.activityType = activityType;
        this.severity = severity;
        this.description = description;
        this.timestamp = timestamp;
    }

    // Getters and setters
    public String getActivityId() {
        return activityId;
    }

    public void setActivityId(String activityId) {
        this.activityId = activityId;
    }

    public String getCustomerId() {
        return customerId;
    }

    public void setCustomerId(String customerId) {
        this.customerId = customerId;
    }

    public String getActivityType() {
        return activityType;
    }

    public void setActivityType(String activityType) {
        this.activityType = activityType;
    }

    public int getSeverity() {
        return severity;
    }

    public void setSeverity(int severity) {
        if (severity < 1) severity = 1;
        if (severity > 5) severity = 5;
        this.severity = severity;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public String getRelatedTransactionId() {
        return relatedTransactionId;
    }

    public void setRelatedTransactionId(String relatedTransactionId) {
        this.relatedTransactionId = relatedTransactionId;
    }

    public String getDetectionMethod() {
        return detectionMethod;
    }

    public void setDetectionMethod(String detectionMethod) {
        this.detectionMethod = detectionMethod;
    }

    public boolean isVerified() {
        return verified;
    }

    public void setVerified(boolean verified) {
        this.verified = verified;
    }

    public String getResolutionStatus() {
        return resolutionStatus;
    }

    public void setResolutionStatus(String resolutionStatus) {
        this.resolutionStatus = resolutionStatus;
    }

    @Override
    public String toString() {
        return "SuspiciousActivity{" +
                "activityId='" + activityId + '\'' +
                ", customerId='" + customerId + '\'' +
                ", activityType='" + activityType + '\'' +
                ", severity=" + severity +
                ", description='" + description + '\'' +
                ", timestamp='" + timestamp + '\'' +
                ", relatedTransactionId='" + relatedTransactionId + '\'' +
                ", detectionMethod='" + detectionMethod + '\'' +
                ", verified=" + verified +
                ", resolutionStatus='" + resolutionStatus + '\'' +
                '}';
    }
}