def get_overall_summary(dt, sections):
    # Compose the final report from all sections in the desired order
    # sections: [news, global, ict, gann, astro]
    return "\n".join(sections)