import plot

if __name__ == "__main__":
    plt = plot.PlotBuilder()

    plt.add_error_text()
    plt.add_glyphs()
    plt.add_axes()

    plt.show()
