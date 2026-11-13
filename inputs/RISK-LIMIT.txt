       IDENTIFICATION DIVISION.
       PROGRAM-ID. RISK-LIMIT.

       ENVIRONMENT DIVISION.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

       01  RISK-CD                 PIC 99 VALUE 01.
           88  RISK-LOW            VALUE 1 THRU 3.
           88  RISK-HIGH           VALUE 5 7 THRU 9.

       01  LIMIT-AMT               PIC 9(7) VALUE 0.

       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
           IF RISK-LOW
               MOVE 500000 TO LIMIT-AMT
           ELSE
               IF RISK-HIGH
                   MOVE 50000 TO LIMIT-AMT
               END-IF
           END-IF

           STOP RUN.