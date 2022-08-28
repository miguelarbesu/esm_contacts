#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc


def calc_contact_df(contact_matrix, probability_threshold=0.05):
    contacts = np.triu(contact_matrix, k=1)
    indexes = np.argwhere(contacts > probability_threshold)
    probabilities = contacts[indexes[:, 0], indexes[:, 1]]

    df = pd.DataFrame(
        {"i": indexes[:, 0], "j": indexes[:, 1], "contact-probability": probabilities}
    )
    df["radius"] = (df["j"] - df["i"]) // 2
    df["center"] = df["i"] + df["radius"]

    return df


def plot_contact_arcs(sequence, contact_df, sequence_offset=0):

    sequence_list = [*sequence]
    mm = 1 / 25.4  # mm in inches
    sequence_length = len(sequence)
    rounded_length = 10 * (sequence_length // 10)
    max_diameter = contact_df["radius"].max() * 2

    if sequence_offset != 0:
        tick_offset = sequence_length - rounded_length
    else:
        tick_offset = 0
    x_start = sequence_offset + tick_offset
    x_end = sequence_length + sequence_offset + tick_offset + 1
    plot_width = 1.5 * rounded_length * mm
    plot_height = plot_width * max_diameter / sequence_length

    fig, ax = plt.subplots(figsize=(plot_width, plot_height))

    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)

    for i, aa in enumerate(sequence_list):
        ax.text(
            x=i + sequence_offset,
            y=0,
            s=aa,
            family="monospace",
            fontsize="xx-small",
            horizontalalignment="center",
            verticalalignment="center",
        )

    for i, row in contact_df.iterrows():
        arc = Arc(
            (row["center"] + sequence_offset, 2),
            row["radius"] * 2,
            row["radius"] * 2,
            theta1=0,
            theta2=180,
            linewidth=1.0,
            alpha=row["contact-probability"],
        )
        ax.add_patch(arc)

    ax.set_ylim(-1, max_diameter * 0.8)
    ax.set_xlim(sequence_offset - 1, sequence_length + sequence_offset + 1)
    ax.set_xticks(
        np.arange(
            x_start - 1,
            x_end - 1,
            10,
        )
    )
    ax.set_xticklabels(
        np.arange(
            x_start,
            x_end,
            10,
        ),
        fontsize="small",
    )

    return fig, ax
