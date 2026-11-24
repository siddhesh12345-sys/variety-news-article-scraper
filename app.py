
import streamlit as st
import pandas as pd
from scraper import search_articles
from datetime import date

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Variety News Article Scraper",
    page_icon="📰",
    layout="wide"
)

# --------------------------------------------------
# DASHBOARD HEADER
# --------------------------------------------------

st.title("📰 Variety News Article Scraper")

st.write(
    "Extract news articles from Variety using their publication date."
)

st.divider()

# --------------------------------------------------
# DATE SELECTION
# --------------------------------------------------

selected_date = st.date_input(
    "Select Article Publication Date",
    value=date.today()
)

# --------------------------------------------------
# SEARCH BUTTON
# --------------------------------------------------

if st.button("🔍 Search Articles", type="primary"):

    target_date = selected_date.strftime("%Y-%m-%d")

    progress = st.progress(0)
    status = st.empty()

    # Progress callback
    def update_progress(current, total, message):

        status.write(message)

        if total > 0:
            progress.progress(
                min(current / total, 1.0)
            )

    try:

        # --------------------------------------------------
        # SEARCH ARTICLES
        # --------------------------------------------------

        with st.spinner("Searching Variety articles..."):

            articles = search_articles(
                target_date,
                update_progress
            )

        progress.progress(1)
        status.success("Search completed!")

        st.divider()

        # --------------------------------------------------
        # SEARCH SUMMARY
        # --------------------------------------------------

        st.subheader("Search Summary")

        col1, col2 = st.columns(2)

        col1.metric(
            "Total Articles Found",
            len(articles)
        )

        col2.metric(
            "Publication Date",
            target_date
        )

        st.divider()

        # --------------------------------------------------
        # DISPLAY ARTICLE DETAILS
        # --------------------------------------------------

        st.subheader("Extracted Article Details")

        if articles:

            df = pd.DataFrame(articles)

            # Required output columns
            required_columns = [
                "Article Date",
                "Title",
                "URL",
                "Main Body Text",
                "Website Name"
            ]

            df = df[required_columns]

            # --------------------------------------------------
            # SAVE CSV FILE
            # --------------------------------------------------

            df.to_csv(
                "articles.csv",
                index=False,
                encoding="utf-8-sig"
            )

            # --------------------------------------------------
            # DISPLAY DATAFRAME
            # --------------------------------------------------

            st.dataframe(
                df,
                width="stretch",
                hide_index=True,
                height=550,
                column_config={

                    "Article Date": st.column_config.TextColumn(
                        "Article Date",
                        width="small"
                    ),

                    "Title": st.column_config.TextColumn(
                        "Title",
                        width="medium"
                    ),

                    "URL": st.column_config.LinkColumn(
                        "URL",
                        display_text="Open Article",
                        width="medium"
                    ),

                    "Main Body Text": st.column_config.TextColumn(
                        "Main Body Text",
                        width="large"
                    ),

                    "Website Name": st.column_config.TextColumn(
                        "Website Name",
                        width="small"
                    )
                }
            )

            # --------------------------------------------------
            # SUCCESS MESSAGE
            # --------------------------------------------------

            st.success(
                f"{len(articles)} article(s) found and saved successfully!"
            )

            # --------------------------------------------------
            # DOWNLOAD CSV
            # --------------------------------------------------

            csv_data = df.to_csv(
                index=False
            ).encode("utf-8-sig")

            st.download_button(
                label="⬇️ Download Complete CSV",
                data=csv_data,
                file_name=f"variety_articles_{target_date}.csv",
                mime="text/csv"
            )

        else:

            st.warning(
                "No articles found for this publication date."
            )

            st.info(
                "Please check the selected date and the availability "
                "of the Variety monthly sitemap."
            )

    except Exception as error:

        st.error(
            f"Search failed: {error}"
        )

        st.info(
            "Check your internet connection and try again."
        )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Data Source: Variety | News Article Scraper Project"
)
