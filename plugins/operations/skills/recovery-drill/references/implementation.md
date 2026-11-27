# Recovery reference

Run restore drills in isolated environments with synthetic or appropriately protected data. Verify backup integrity, decryption keys, privileges, extensions, application smoke checks and expected/control cohorts. A successful backup job is not evidence that restore works.

Credential compromise, data corruption, provider outage and deployment regression require different runbooks. A roll-forward application fix does not repair already-corrupted records; a database restore can reintroduce data that was deleted under policy. Explicitly reconcile these constraints.
