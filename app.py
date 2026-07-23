import csv
import io

import streamlit as st

from src.database.database import (
    delete_university,
    get_saved_universities,
    get_saved_university_count,
    get_search_history,
    get_total_searches,
    save_search,
    save_university,
)
from src.services.university_service import search_universities

st.set_page_config(page_title="School Check", page_icon="🎓", layout="wide")

st.title("🎓 School Check")
st.caption("Search universities, review your history, and manage saved institutions.")


def render_dashboard() -> None:
    """Show a concise overview of recent activity."""
    st.subheader("Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Searches", get_total_searches())
    c2.metric("Saved Universities", get_saved_university_count())
    c3.metric("Recent History", min(get_total_searches(), 10))

    st.info("Use the navigation panel to search for universities, review history, or manage saved entries.")

    recent_history = get_search_history(limit=5)
    if recent_history:
        st.subheader("Recent Searches")
        st.dataframe(recent_history, use_container_width=True, hide_index=True)


def render_university_search() -> None:
    """Search universities and allow saving matching results."""
    st.subheader("Search Universities")

    university = st.text_input("University Name")
    country = st.text_input("Country")

    if st.button("Search", use_container_width=True):
        if not university.strip() and not country.strip():
            st.warning("Enter a university name or country to begin a search.")
            return

        try:
            save_search(university, country)
            with st.spinner("Searching..."):
                schools = search_universities(university, country)
        except Exception as exc:  # pragma: no cover - UI safety net
            st.error(f"Unable to complete the search right now: {exc}")
            return

        if not schools:
            st.info("No universities matched the supplied criteria.")
            return

        st.success(f"Found {len(schools)} universities")

        for index, school in enumerate(schools):
            with st.container(border=True):
                st.markdown(f"### {school['name']}")
                st.write("Country:", school["country"])

                if school.get("domains"):
                    st.write("Domain:", school["domains"][0])

                website = school["web_pages"][0] if school.get("web_pages") else ""
                domain = school["domains"][0] if school.get("domains") else ""

                col1, col2 = st.columns(2)
                with col1:
                    if website:
                        st.link_button("Official Website", website)
                with col2:
                    if st.button("Save University", key=f"save-{index}-{school['name']}"):
                        try:
                            saved = save_university(school["name"], school["country"], domain, website)
                        except Exception as exc:  # pragma: no cover - UI safety net
                            st.error(f"Unable to save this university: {exc}")
                            return

                        if saved:
                            st.success("University saved successfully.")
                        else:
                            st.info("This university is already saved.")


def render_saved_universities() -> None:
    """List saved universities and allow deletion or CSV export."""
    st.subheader("Saved Universities")

    saved_universities = get_saved_universities()
    if not saved_universities:
        st.info("You have not saved any universities yet.")
        return

    rows = []
    for row in saved_universities:
        rows.append(
            {
                "name": row[0],
                "country": row[1],
                "domain": row[2],
                "website": row[3],
                "saved_at": row[4],
            }
        )

    st.dataframe(rows, use_container_width=True, hide_index=True)

    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=["name", "country", "domain", "website", "saved_at"])
    writer.writeheader()
    writer.writerows(rows)

    st.download_button(
        label="Export to CSV",
        data=csv_buffer.getvalue().encode("utf-8"),
        file_name="saved_universities.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.divider()
    st.subheader("Delete Saved Universities")
    for university in rows:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{university['name']} — {university['country']}")
        with col2:
            if st.button("Delete", key=f"delete-{university['name']}"):
                try:
                    deleted = delete_university(university["name"])
                except Exception as exc:  # pragma: no cover - UI safety net
                    st.error(f"Unable to delete this university: {exc}")
                    return

                if deleted:
                    st.success("University removed from your saved list.")
                    st.rerun()
                else:
                    st.warning("The university could not be removed.")


def render_search_history() -> None:
    """Show the recent search history stored by the app."""
    st.subheader("Search History")
    history = get_search_history(limit=20)

    if not history:
        st.info("No search history has been recorded yet.")
        return

    st.dataframe(history, use_container_width=True, hide_index=True)


def render_weekly_report() -> None:
    """Display a simple weekly verification report simulation using current data."""
    st.subheader("Weekly Verification Report")
    st.caption("A lightweight simulation based on the current saved records and recent searches.")

    total_searches = get_total_searches()
    saved_count = get_saved_university_count()

    c1, c2, c3 = st.columns(3)
    c1.metric("Searches This Week", total_searches)
    c2.metric("Saved Universities", saved_count)
    c3.metric("Verification Status", "Ready" if saved_count else "Pending")

    st.markdown("### Verification Summary")
    st.write(
        "The weekly verification simulation reviews the latest saved entries and confirms that the system is ready for follow-up checks."
    )

    verification_rows = [
        {"Check": "Search logging", "Status": "Completed", "Notes": "Recent searches are being recorded."},
        {"Check": "Duplicate prevention", "Status": "Completed", "Notes": "Saved universities are checked before insert."},
        {"Check": "Export workflow", "Status": "Completed", "Notes": "Saved universities can be exported as CSV."},
    ]
    st.dataframe(verification_rows, use_container_width=True, hide_index=True)


with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Go to",
        [
            "Dashboard",
            "Universities",
            "Search History",
            "Saved Universities",
            "Weekly Report",
            "Courses",
            "Scholarships",
            "Visa",
        ],
    )


if page == "Dashboard":
    render_dashboard()
elif page == "Universities":
    render_university_search()
elif page == "Saved Universities":
    render_saved_universities()
elif page == "Search History":
    render_search_history()
elif page == "Weekly Report":
    render_weekly_report()
else:
    st.info(f"🚧 {page} module coming next.")
