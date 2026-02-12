install:
	@pip install -e .

# Runs the main extraction
data:
	@python -m patek_analysis.data

# Runs the ML bonus
model:
	@python -m patek_analysis.model

# Runs the API extraction 
fx:
	@python -m patek_analysis.fx_rates


clean:
	@rm -f *.csv
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "🧹 Removed old CSV files and cache. Ready to restart."