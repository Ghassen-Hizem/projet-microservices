package root.finrisk.client;

import org.apache.axis2.client.Options;
import org.apache.axis2.addressing.EndpointReference;
import org.apache.axis2.rpc.client.RPCServiceClient;

import root.finrisk.service.CustomerFinancialProfile;
import root.finrisk.service.Transaction;
import root.finrisk.service.SuspiciousActivity;

import javax.xml.namespace.QName;

/**
 * Example client that demonstrates how to call the SOAP service
 */
public class CustomerFinancialProfileClient {

    public static void main(String[] args) {
        try {
            // Create the client
            RPCServiceClient client = new RPCServiceClient();
            Options options = client.getOptions();

            // Set the endpoint URL
            EndpointReference targetEPR =
                    new EndpointReference("http://localhost:8080/customer-financial-profile-service/services/CustomerFinancialProfileService");
            options.setTo(targetEPR);

            // Prepare to call the service
            QName operationQName = new QName("http://service.finrisk.com", "getCustomerFinancialProfile");

            // Define parameters - customer ID to look up
            Object[] params = new Object[] { "C1001" };

            // Define return type
            Class<?>[] returnTypes = new Class[] { CustomerFinancialProfile.class };

            // Invoke the service
            Object[] response = client.invokeBlocking(operationQName, params, returnTypes);

            // Process the response
            if (response != null && response.length > 0 && response[0] != null) {
                CustomerFinancialProfile profile = (CustomerFinancialProfile) response[0];

                System.out.println("Customer ID: " + profile.getCustomerId());
                System.out.println("Customer Name: " + profile.getCustomerName());
                System.out.println("Account Age (months): " + profile.getAccountAge());
                System.out.println("Credit Score: " + profile.getCreditScore());

                System.out.println("\nTransactions:");
                for (Transaction tx : profile.getTransactions()) {
                    System.out.println("  - ID: " + tx.getTransactionId() +
                            ", Type: " + tx.getType() +
                            ", Amount: $" + tx.getAmount() +
                            ", Country: " + tx.getCountry() +
                            ", Date: " + tx.getTimestamp());
                }

                System.out.println("\nSuspicious Activities:");
                for (SuspiciousActivity activity : profile.getSuspiciousActivities()) {
                    System.out.println("  - ID: " + activity.getActivityId() +
                            ", Type: " + activity.getActivityType() +
                            ", Severity: " + activity.getSeverity() +
                            ", Description: " + activity.getDescription());
                }

                // Calculate risk score based on various factors
                int riskScore = calculateRiskScore(profile);
                System.out.println("\nCalculated Risk Score: " + riskScore + "/100");
                System.out.println("Risk Category: " + getRiskCategory(riskScore));
            } else {
                System.out.println("No profile found for the given customer ID.");
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Calculate a risk score based on customer financial profile
     *
     * @param profile The customer's financial profile
     * @return A risk score from 0-100 (higher means higher risk)
     */
    private static int calculateRiskScore(CustomerFinancialProfile profile) {
        int score = 0;

        // Factor 1: Credit score
        if (profile.getCreditScore() < 600) score += 25;
        else if (profile.getCreditScore() < 700) score += 15;
        else if (profile.getCreditScore() < 750) score += 5;

        // Factor 2: Account age
        if (profile.getAccountAge() < 12) score += 20;
        else if (profile.getAccountAge() < 24) score += 10;
        else if (profile.getAccountAge() < 36) score += 5;

        // Factor 3: Suspicious activities
        for (SuspiciousActivity activity : profile.getSuspiciousActivities()) {
            score += activity.getSeverity() * 5;
        }

        // Factor 4: Foreign transactions
        int foreignTransactions = 0;
        for (Transaction tx : profile.getTransactions()) {
            if (!tx.getCountry().equals("USA")) {
                foreignTransactions++;
            }
        }

        if (foreignTransactions > 2) score += 15;
        else if (foreignTransactions > 0) score += 10;

        // Cap the score at 100
        return Math.min(score, 100);
    }

    /**
     * Get a risk category based on the numerical score
     */
    private static String getRiskCategory(int score) {
        if (score < 20) return "Low Risk";
        else if (score < 50) return "Medium Risk";
        else if (score < 75) return "High Risk";
        else return "Extreme Risk";
    }
}