# Summary of Corrections Applied

The following corrections were identified and applied to
`simulator.js`:

1. **Cant vertical error sign (line 93).**
    The original code computed
    `shiftY\_mm = -totalComp\_mm * (1 - Math.cos(cant))`,
    yielding a negative value that moved the impact *upward*
    on the canvas.  Physically, canting always lowers the impact
    (*Rifle Cant*).  In Canvas coordinates ($+y$ down), the
    correct expression is
    `shiftY\_mm = totalComp\_mm * (1 - Math.cos(cant))`,
    which is non-negative and moves the impact downward.
2. **Scoring offset (line 113).**
    The original formula `10.9 - dist\_mm / 2.5` evaluated to
    9.9 at the 10-ring boundary (2.5 mm), whereas ISSF rules score
    this as 10.0.  The corrected formula
    `Math.min(10.9, 11.0 - dist\_mm / 2.5)` aligns the ring
    boundaries with integer scores and caps the maximum at 10.9.
3. **Cant error and sight height (2026-11-12).**
    The code and this document took the cant error as
    $(H + h_g)\sin\theta$, the sight height added to the drop.  At the
    zeroing distance the sight height cancels (*Rifle Cant*): the
    error is $h_g\sin\theta$.  The former value was 4.7 times too large
    at 10 m (2.7 mm instead of 0.56 mm for a 2$^\circ$ cant) and
    1.5 times too large at 50 m (6.0 mm instead of 3.9 mm).  The
    cant now also turns the click correction, which is fixed to the
    rifle.

The backup file `simulator.best.js` retains the original code
for reference.

\begin{thebibliography}{10}

\bibitem{mccoy}
  R. L. McCoy,
  *Modern Exterior Ballistics: The Launch and Flight Dynamics
  of Symmetric Projectiles*,
  2nd ed. Schiffer Publishing, 2012.
  ISBN 978-0-7643-3825-0.

\bibitem{litz}
  B. Litz,
  *Applied Ballistics for Long-Range Shooting*,
  3rd ed. Applied Ballistics LLC, 2015.
  ISBN 978-0-9909206-1-8.

\bibitem{issf}
  International Shooting Sport Federation,
  *ISSF Rule Book*, Edition 2026
  (First Print 12/2025, effective 1 January 2026).
  [https://www.issf-sports.org/rules](https://www.issf-sports.org/rules)

\bibitem{hecht}
  E. Hecht,
  *Optics*,
  5th ed. Pearson, 2017.
  ISBN 978-0-13-397722-6.

\bibitem{smith}
  W. J. Smith,
  *Modern Optical Engineering*,
  4th ed. McGraw-Hill, 2007.
  ISBN 978-0-07-147687-4.

\bibitem{rinker}
  R. A. Rinker,
  *Understanding Firearm Ballistics: Basic to Advanced
  Ballistics*,
  6th ed. Mulberry House Publishing, 2005.
  ISBN 978-0-9645598-5-1.

\bibitem{mann}
  F. W. Mann,
  *The Bullet's Flight from Powder to Target*,
  Wolfe Publishing, 1909 (reprinted 2009).
  ISBN 978-0-935632-04-0.

\bibitem{pejsa}
  A. J. Pejsa,
  *Modern Practical Ballistics*,
  2nd ed. Kenwood Publishing, 1991.
  ISBN 978-0-9612776-3-5.

\bibitem{nra}
  National Rifle Association,
  *NRA Guide to Rifle Marksmanship*,
  NRA Publications, 2014.

\bibitem{hatcher}
  J. S. Hatcher,
  *Hatcher's Notebook*,
  3rd ed. Stackpole Books, 1962.
  ISBN 978-0-8117-0795-4.

\end{thebibliography}