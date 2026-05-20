Feature: Pet lifecycle management
  As a pet store operator
  I want to manage pets through their full lifecycle
  So that the inventory stays accurate

  Scenario: Create a new pet
    Given I have a pet payload with name "BDDPet" and status "available"
    When I send a POST request to create the pet
    Then the response status should be 200
    And the pet name should be "BDDPet"
    And the pet status should be "available"

  Scenario: Update an existing pet
    Given a pet exists in the store
    When I update the pet status to "pending"
    Then the response status should be 200
    And the pet status should be "pending"

  Scenario: Delete a pet
    Given a pet exists in the store
    When I delete the pet
    Then the response status should be 200
    And the pet should no longer be found
