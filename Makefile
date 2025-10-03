# SnowSQL Connection Helper

# Variables
SNOWSQL_PATH = /Applications/SnowSQL.app/Contents/MacOS/snowsql
ACCOUNT = CYBERAGENT-INFOSYS_DATA
USER = S27928
AUTHENTICATOR = externalbrowser
ROLE = ACCOUNTADMIN

# Default target
.PHONY: help
help:
	@echo "SnowSQL Connection Helper"
	@echo ""
	@echo "Available commands:"
	@echo "  make connect    - Connect to Snowflake"
	@echo "  make test       - Test connection with a simple query"
	@echo "  make version    - Show SnowSQL version"

# Connect to Snowflake
.PHONY: connect
connect:
	$(SNOWSQL_PATH) -a $(ACCOUNT) -u $(USER) --authenticator $(AUTHENTICATOR) -r $(ROLE)

# Test connection
.PHONY: test
test:
	$(SNOWSQL_PATH) -a $(ACCOUNT) -u $(USER) --authenticator $(AUTHENTICATOR) -r $(ROLE) -q "SELECT CURRENT_USER(), CURRENT_ROLE();"

# Show version
.PHONY: version
version:
	$(SNOWSQL_PATH) --version