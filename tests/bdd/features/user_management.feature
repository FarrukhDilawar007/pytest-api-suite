Feature: User account management
  As a pet store customer
  I want to manage my account
  So that I can access the store

  Scenario: Create a new user account
    Given I have a user payload with username "bdd_user_001"
    When I send a POST request to create the user
    Then the user creation response status should be 200
    And the user "bdd_user_001" should exist in the system

  Scenario: Login with valid credentials
    Given a user "bdd_login_user" exists with password "Password123"
    When I login with username "bdd_login_user" and password "Password123"
    Then the login response status should be 200
    And the response should contain a session token
