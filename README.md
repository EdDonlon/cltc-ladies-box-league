# Charleville LTC Padel Box League Sep-Nov 2026

A simple Streamlit app showing live results & leag tables for a padel box league.


### How to run it on your own machine

1. Install the requirements:

   ```
   pip install -r requirements.txt
   ```

2. Create `.streamlit/secrets.toml` with the Google Sheets configuration:

   ```
   [sheets]
   spreadsheet_id = "your-spreadsheet-id"
   tolka_gid = "your-tolka-tab-id"
   liffey_gid = "your-liffey-tab-id"
   ```

   Keep this file private; it is excluded from Git.

3. Run the app:

   ```
   streamlit run streamlit_app.py
   ```

For Streamlit Community Cloud, add the same TOML configuration under the app's
**Settings > Secrets** instead of committing the local secrets file.
