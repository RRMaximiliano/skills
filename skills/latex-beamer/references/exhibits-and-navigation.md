# Exhibits, references, and navigation

## Standard table frame

Keep imported Stata/R fragments unchanged. The caption and notes live in the slide source.

```latex
\begin{frame}[label=results-table]{Main Results}
  \begin{table}
    \centering
    \singlespacing
    \small
    \adjustbox{max width=\textwidth,max totalheight=0.72\textheight}{%
      \begin{threeparttable}
        \caption{Descriptive table title}\label{tab:main_results}
        \input{Tabs/main_results.tex}
        \begin{tablenotes}
          \setlength\labelsep{0pt}
          \footnotesize
          \item \textit{Notes}: Explain the estimand, sample, specification,
          inference, and significance notation.
        \end{tablenotes}
      \end{threeparttable}%
    }
  \end{table}
\end{frame}
```

The `threeparttable` sits inside `adjustbox`, so caption, tabular body, and notes share the table's width. Load `caption` with `skip=0pt`; the style also removes `threeparttable`'s internal post-caption gap so the top rule follows the title directly. Never place the note outside this wrapper. If the full table becomes unreadable, prepare a slide-specific fragment only when the user supplies or explicitly requests it; otherwise use a descriptive placeholder and link the complete table in the appendix.

## Standard figure frame

```latex
\begin{frame}{Main Result}
  \begin{figure}
    \caption{Descriptive figure title}\label{fig:main_result}
    \centering
    \includegraphics[width=0.88\linewidth,height=0.63\textheight,keepaspectratio]{Figs/result.pdf}
    \fnote{\textit{Notes}: Explain the sample, estimand, intervals, and source.}
  \end{figure}
\end{frame}
```

Keep the caption above and the justified note below. Notes should be footnote size but readable when projected.

## Buttons

Inline:

```latex
\goto{appendix-identification}{Details}
\backto{main-identification}{Back to empirical strategy}
```

Bottom-left is the default position. Give every button an informative label:

```latex
\bottomleft{\goto{appendix-identification}{Identification details}}
\bottomleft{\backto{main-results}{Back to main results} \quad \goto{appendix-table}{Full table}}
\topright{\goto<2->{appendix-robustness}{Robustness checks}}
```

All four positioned controls use the same horizontal grid as the slide text. The top pair shares one baseline below the frame title, and the bottom pair shares one baseline above the slide counter. Do not introduce a one-off offset for a single corner; move the shared pair when a layout genuinely requires more clearance.

Targets are normally frame labels:

```latex
\begin{frame}[label=appendix-identification]{Identification Details}
```

The position wrappers also accept brief non-button content. Without a position wrapper, a button remains inline. Other positions remain available when requested or needed by the layout. Avoid a bare label such as `Back`; name the frame or section being restored. Validate every target in the compiled PDF.

## References

Use one ordinary frame when the bibliography fits:

```latex
\begin{frame}{References}
  \bibliographystyle{aer}
  \bibliography{references}
\end{frame}
```

For a long bibliography, use automatic frame breaks and Roman continuation titles:

```latex
\begin{frame}[allowframebreaks]{References \insertcontinuationcountroman}
  \bibliographystyle{aer}
  \bibliography{references}
\end{frame}
```

Do not use page-backreferences in slides.
