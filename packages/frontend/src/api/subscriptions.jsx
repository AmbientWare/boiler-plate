import client from "./client";

const subscriptionApi = {
  getUserSubscription,
  getUserSubscriptionUsage,
  getUerPortal,
  getSubscriptionOptions,
};

export default subscriptionApi;

function getUserSubscription() {
  return client.get("/subscriptions/user");
}

function getUserSubscriptionUsage() {
  return client.get("/subscriptions/user/usage");
}

function getUerPortal() {
  return client.get("/subscriptions/portal");
}

function getSubscriptionOptions() {
  return client.get("/subscriptions/plans");
}
