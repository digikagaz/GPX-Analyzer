import streamlit as st
import matplotlib.pyplot as plt

def show_segment_summary_and_details(df, full_df, kind="climb"):
    """Display detailed segment (climb/descent) summaries with slope distribution and elevation profile."""
    
    # Required columns check
    required_cols = [
        "start_km", "end_km", "length_m", "avg_slope",
        "min_slope", "max_slope", "category", "start_idx", "end_idx"
    ]
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
            f"📐 **Average Slope:** {row['avg_slope']:.1f} %\n"
            f"📉 **Min Slope:** {row['min_slope']:.1f} %\n"
            f"📈 **Max Slope:** {row['max_slope']:.1f} %\n"
            f"🏷️ **Category:** {row['category']}"
        )

        with st.expander(f"🔽 {title}"):
            st.markdown(summary)
            
            if "plot_grade" in full_df.columns:
                # Extract segment data
                segment_df = full_df.iloc[int(row["start_idx"]):int(row["end_idx"]) + 1]

                # Create two plots side-by-side
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.5))

                # Left: slope histogram
                ax1.hist(segment_df["plot_grade"], bins=15, color="gray", edgecolor="black")
                ax1.set_xlabel("Slope (%)")
                ax1.set_ylabel("Frequency")
                ax1.set_title("Slope Distribution")

                # Right: elevation profile
                if "elevation" in segment_df.columns:
                    x = segment_df["distance_km"] - segment_df["distance_km"].iloc[0]
                    ax2.plot(x, segment_df["elevation"], color="tab:red")
                    ax2.set_xlabel("Distance (km)")
                    ax2.set_ylabel("Elevation (m)")
                    ax2.set_title("Elevation Profile")
                else:
                    ax2.text(0.5, 0.5, "No elevation data", ha="center", va="center", fontsize=10)
                    ax2.set_axis_off()

                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.warning("No 'plot_grade' column found in full_df.")
