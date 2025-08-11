import streamlit as st
import matplotlib.pyplot as plt

def show_segment_summary_and_details(df, full_df, kind="climb"):
    required_cols = ["start_km", "end_km", "length_m", "avg_slope", "min_slope", "max_slope", "category", "start_idx", "end_idx"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"Missing columns in {kind} DataFrame: {', '.join(missing)}")
        return

    if df.empty:
        st.info(f"No {kind}s detected.")
        return

    for idx, row in df.reset_index(drop=True).iterrows():
        elev_change = row.get("elev_gain", row.get("elev_loss", 0))
        title = f"{kind.capitalize()} {idx+1} • {row['length_m']:.0f} m, {elev_change:.0f} m"

        summary = (
            f"📍 **Start:** {row['start_km']:.2f} km\n"
            f"🏁 **End:** {row['end_km']:.2f} km\n"
            f"📏 **Length:** {row['length_m']:.0f} m\n"
            f"⛰️ **Gain/Loss:** {elev_change:.1f} m\n"
            f"📐 **Avg Slope:** {row['avg_slope']:.1f} %\n"
            f"📉 **Min Slope:** {row['min_slope']:.1f} %\n"
            f"📈 **Max Slope:** {row['max_slope']:.1f} %\n"
            f"🏷️ **Category:** {row['category']}"
        )

        with st.expander(f"🔽 {title}"):
            st.markdown(summary)
            if "plot_grade" in full_df.columns:
                grades = full_df["plot_grade"].iloc[int(row["start_idx"]):int(row["end_idx"])+1]
                fig, ax = plt.subplots(figsize=(6, 2.5))
                ax.hist(grades, bins=15, color="gray", edgecolor="black")
                ax.set_xlabel("Pendiente (%)")
                ax.set_ylabel("Frecuencia")
                ax.set_title("Histograma de pendientes")
                st.pyplot(fig)
            else:
                st.warning("No 'plot_grade' column found in full_df.")
